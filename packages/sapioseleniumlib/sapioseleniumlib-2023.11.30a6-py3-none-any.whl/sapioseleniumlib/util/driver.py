"""
This class includes the driver functions including tracking of states and web driver for Selenium.
"""
from __future__ import annotations

import logging
import os
import os.path
import re
import tempfile
import time
from enum import Enum
from pathlib import Path
from time import sleep
from typing import List, Callable, Any, Type

from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.utils import keys_to_typing
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import staleness_of, AnyDriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager

TOASTR_XPATH: str = "//body/*[@id=\"toast-container\"]"


class BrowserType(Enum):
    """
    All browser types we support in web driver.
    """
    CHROME = 0
    SAFARI = 1
    FIREFOX = 2
    EDGE = 3


class SapioTestDriverFileManager:
    _storage_dir_path: str
    _screenshot_dir: str
    _download_dir: str
    _browser_profile_dir: str
    _temp_files_to_delete: list[str]

    def __init__(self, storage_dir_path: Optional[str] = None):
        if not storage_dir_path:
            storage_dir_path = os.path.join(Path.home(), 'sapio_selenium_runs')
        self._storage_dir_path = storage_dir_path
        self._screenshot_dir = os.path.join(storage_dir_path, 'screenshots')
        self._download_dir = os.path.join(storage_dir_path, 'downloads')
        self._browser_profile_dir = os.path.join(storage_dir_path, "browser_profile")
        self._temp_files_to_delete = []
        os.makedirs(self._screenshot_dir, exist_ok=True)
        os.makedirs(self._download_dir, exist_ok=True)
        os.makedirs(self._browser_profile_dir, exist_ok=True)

    def on_stop(self):
        for f in self._temp_files_to_delete:
            logging.info("Delete temp file on stop: " + f)
            os.remove(f)

    @property
    def storage_location_path(self) -> str:
        return self._storage_dir_path

    @property
    def screenshot_dir(self) -> str:
        return self._screenshot_dir

    @property
    def download_dir(self) -> str:
        return self._download_dir

    @property
    def browser_profile_dir(self):
        return self._browser_profile_dir

    def upload_temp_bytes(self, file_prefix: str, file_data: bytes) -> str:
        with tempfile.NamedTemporaryFile(prefix=file_prefix, suffix=".xlsx", mode='wb',
                                         delete=False) as f:
            self._temp_files_to_delete.append(f.name)
            f.write(file_data)
            return f.name

    def get_last_downloaded_file(self) -> Optional[str]:
        """
        Find the latest created file by created date.
        """
        files = os.listdir(self.download_dir)
        paths = [os.path.join(self.download_dir, basename) for basename in files]
        if not paths:
            return None
        latest_file_path = max(paths, key=os.path.getctime)
        # Wait until the file has done writing if it's not done yet. We check that by comparing file sizes.
        last_file_length = os.path.getsize(latest_file_path)
        while True:
            time.sleep(1)
            cur_file_length = os.path.getsize(latest_file_path)
            if last_file_length == cur_file_length:
                return latest_file_path
            last_file_length = cur_file_length


class SapioSeleniumDriver:
    _driver: WebDriver
    __scroll_button_offset: int
    _browser_type: BrowserType
    _file_man: SapioTestDriverFileManager

    @property
    def file_man(self) -> SapioTestDriverFileManager:
        """
        Sapio selenium testing file manager for file I/O.
        """
        return self._file_man

    @property
    def selenium_driver(self):
        """
        The underlying selenium driver inside this object.
        """
        return self._driver

    @property
    def browser_type(self):
        """
        The browser type this driver is supporting.
        """
        return self._browser_type

    def __init__(self, browser_type: BrowserType, url: str, headless: bool,
                 file_man: None | SapioTestDriverFileManager = None,
                 browser_binary_location: str | None = None):
        # scroll offset is 6 except in case of firefox.
        self.__scroll_button_offset = 6
        self._browser_type = browser_type
        if not file_man:
            path: str = os.path.join(Path.home(), 'sapio_selenium_runs')
            file_man = SapioTestDriverFileManager(path)
        self._file_man = file_man
        if browser_type == BrowserType.CHROME:
            options = webdriver.ChromeOptions()
            if browser_binary_location:
                options.binary_location = browser_binary_location
            options.add_experimental_option("prefs", {
                "download.default_directory": file_man.download_dir,
                "download.prompt_for_download": False,
                # Boolean that records if the download directory was changed by an upgrade
                # a unsafe location to a safe location.
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            })
            options.add_argument("--user-data-dir=" + file_man.browser_profile_dir)
            if headless:
                options.add_argument('--headless')
                options.add_argument('--disable-gpu')
            self.__configure_common_options(options)
            self._driver = webdriver.Chrome(options)
        elif browser_type == BrowserType.SAFARI:
            raise ValueError("We don't support Safari right now with this framework.. Sorry.")
        elif browser_type == BrowserType.FIREFOX:
            options = FirefoxOptions()
            if browser_binary_location:
                options.binary_location = browser_binary_location
            # folderList 2 tells it to not use default Downloads directory.
            options.set_preference("browser.download.folderList", 2)
            # turns off download progress bar pop up
            options.set_preference('browser.download.manager.showWhenStarting', False)
            # set download manager directory
            options.set_preference('browser.download.dir', file_man.download_dir)
            # don't pop an alert about untrusted file for these file types, prevent dm overlay causing click interrupt.
            options.set_preference("browser.download.animateNotifications", False)
            options.set_preference('browser.download.alwaysOpenPanel', False)
            options.set_preference('browser.download.autohideButton', False)
            options.set_preference('browser.download.panel.shown', True)
            options.set_preference('browser.download.alwaysOpenInSystemViewerContextMenuItem', False)
            options.set_preference("services.sync.prefs.sync.browser.download.manager.showWhenStarting", False)
            options.set_preference("browser.helperApps.neverAsk.saveToDisk",
                                   "application/vnd.hzn-3d-crossword;video/3gpp;video/3gpp2;application/vnd.mseq;application/vnd.3m.post-it-notes;application/vnd.3gpp.pic-bw-large;application/vnd.3gpp.pic-bw-small;application/vnd.3gpp.pic-bw-var;application/vnd.3gp2.tcap;application/x-7z-compressed;application/x-abiword;application/x-ace-compressed;application/vnd.americandynamics.acc;application/vnd.acucobol;application/vnd.acucorp;audio/adpcm;application/x-authorware-bin;application/x-athorware-map;application/x-authorware-seg;application/vnd.adobe.air-application-installer-package+zip;application/x-shockwave-flash;application/vnd.adobe.fxp;application/pdf;application/vnd.cups-ppd;application/x-director;applicaion/vnd.adobe.xdp+xml;application/vnd.adobe.xfdf;audio/x-aac;application/vnd.ahead.space;application/vnd.airzip.filesecure.azf;application/vnd.airzip.filesecure.azs;application/vnd.amazon.ebook;application/vnd.amiga.ami;applicatin/andrew-inset;application/vnd.android.package-archive;application/vnd.anser-web-certificate-issue-initiation;application/vnd.anser-web-funds-transfer-initiation;application/vnd.antix.game-component;application/vnd.apple.installe+xml;application/applixware;application/vnd.hhe.lesson-player;application/vnd.aristanetworks.swi;text/x-asm;application/atomcat+xml;application/atomsvc+xml;application/atom+xml;application/pkix-attr-cert;audio/x-aiff;video/x-msvieo;application/vnd.audiograph;image/vnd.dxf;model/vnd.dwf;text/plain-bas;application/x-bcpio;application/octet-stream;image/bmp;application/x-bittorrent;application/vnd.rim.cod;application/vnd.blueice.multipass;application/vnd.bm;application/x-sh;image/prs.btif;application/vnd.businessobjects;application/x-bzip;application/x-bzip2;application/x-csh;text/x-c;application/vnd.chemdraw+xml;text/css;chemical/x-cdx;chemical/x-cml;chemical/x-csml;application/vn.contact.cmsg;application/vnd.claymore;application/vnd.clonk.c4group;image/vnd.dvb.subtitle;application/cdmi-capability;application/cdmi-container;application/cdmi-domain;application/cdmi-object;application/cdmi-queue;applicationvnd.cluetrust.cartomobile-config;application/vnd.cluetrust.cartomobile-config-pkg;image/x-cmu-raster;model/vnd.collada+xml;text/csv;application/mac-compactpro;application/vnd.wap.wmlc;image/cgm;x-conference/x-cooltalk;image/x-cmx;application/vnd.xara;application/vnd.cosmocaller;application/x-cpio;application/vnd.crick.clicker;application/vnd.crick.clicker.keyboard;application/vnd.crick.clicker.palette;application/vnd.crick.clicker.template;application/vn.crick.clicker.wordbank;application/vnd.criticaltools.wbs+xml;application/vnd.rig.cryptonote;chemical/x-cif;chemical/x-cmdf;application/cu-seeme;application/prs.cww;text/vnd.curl;text/vnd.curl.dcurl;text/vnd.curl.mcurl;text/vnd.crl.scurl;application/vnd.curl.car;application/vnd.curl.pcurl;application/vnd.yellowriver-custom-menu;application/dssc+der;application/dssc+xml;application/x-debian-package;audio/vnd.dece.audio;image/vnd.dece.graphic;video/vnd.dec.hd;video/vnd.dece.mobile;video/vnd.uvvu.mp4;video/vnd.dece.pd;video/vnd.dece.sd;video/vnd.dece.video;application/x-dvi;application/vnd.fdsn.seed;application/x-dtbook+xml;application/x-dtbresource+xml;application/vnd.dvb.ait;applcation/vnd.dvb.service;audio/vnd.digital-winds;image/vnd.djvu;application/xml-dtd;application/vnd.dolby.mlp;application/x-doom;application/vnd.dpgraph;audio/vnd.dra;application/vnd.dreamfactory;audio/vnd.dts;audio/vnd.dts.hd;imag/vnd.dwg;application/vnd.dynageo;application/ecmascript;application/vnd.ecowin.chart;image/vnd.fujixerox.edmics-mmr;image/vnd.fujixerox.edmics-rlc;application/exi;application/vnd.proteus.magazine;application/epub+zip;message/rfc82;application/vnd.enliven;application/vnd.is-xpr;image/vnd.xiff;application/vnd.xfdl;application/emma+xml;application/vnd.ezpix-album;application/vnd.ezpix-package;image/vnd.fst;video/vnd.fvt;image/vnd.fastbidsheet;application/vn.denovo.fcselayout-link;video/x-f4v;video/x-flv;image/vnd.fpx;image/vnd.net-fpx;text/vnd.fmi.flexstor;video/x-fli;application/vnd.fluxtime.clip;application/vnd.fdf;text/x-fortran;application/vnd.mif;application/vnd.framemaker;imae/x-freehand;application/vnd.fsc.weblaunch;application/vnd.frogans.fnc;application/vnd.frogans.ltf;application/vnd.fujixerox.ddd;application/vnd.fujixerox.docuworks;application/vnd.fujixerox.docuworks.binder;application/vnd.fujitu.oasys;application/vnd.fujitsu.oasys2;application/vnd.fujitsu.oasys3;application/vnd.fujitsu.oasysgp;application/vnd.fujitsu.oasysprs;application/x-futuresplash;application/vnd.fuzzysheet;image/g3fax;application/vnd.gmx;model/vn.gtw;application/vnd.genomatix.tuxedo;application/vnd.geogebra.file;application/vnd.geogebra.tool;model/vnd.gdl;application/vnd.geometry-explorer;application/vnd.geonext;application/vnd.geoplan;application/vnd.geospace;applicatio/x-font-ghostscript;application/x-font-bdf;application/x-gtar;application/x-texinfo;application/x-gnumeric;application/vnd.google-earth.kml+xml;application/vnd.google-earth.kmz;application/vnd.grafeq;image/gif;text/vnd.graphviz;aplication/vnd.groove-account;application/vnd.groove-help;application/vnd.groove-identity-message;application/vnd.groove-injector;application/vnd.groove-tool-message;application/vnd.groove-tool-template;application/vnd.groove-vcar;video/h261;video/h263;video/h264;application/vnd.hp-hpid;application/vnd.hp-hps;application/x-hdf;audio/vnd.rip;application/vnd.hbci;application/vnd.hp-jlyt;application/vnd.hp-pcl;application/vnd.hp-hpgl;application/vnd.yamaha.h-script;application/vnd.yamaha.hv-dic;application/vnd.yamaha.hv-voice;application/vnd.hydrostatix.sof-data;application/hyperstudio;application/vnd.hal+xml;text/html;application/vnd.ibm.rights-management;application/vnd.ibm.securecontainer;text/calendar;application/vnd.iccprofile;image/x-icon;application/vnd.igloader;image/ief;application/vnd.immervision-ivp;application/vnd.immervision-ivu;application/reginfo+xml;text/vnd.in3d.3dml;text/vnd.in3d.spot;mode/iges;application/vnd.intergeo;application/vnd.cinderella;application/vnd.intercon.formnet;application/vnd.isac.fcs;application/ipfix;application/pkix-cert;application/pkixcmp;application/pkix-crl;application/pkix-pkipath;applicaion/vnd.insors.igm;application/vnd.ipunplugged.rcprofile;application/vnd.irepository.package+xml;text/vnd.sun.j2me.app-descriptor;application/java-archive;application/java-vm;application/x-java-jnlp-file;application/java-serializd-object;text/x-java-source,java;application/javascript;application/json;application/vnd.joost.joda-archive;video/jpm;image/jpeg;video/jpeg;application/vnd.kahootz;application/vnd.chipnuts.karaoke-mmd;application/vnd.kde.karbon;aplication/vnd.kde.kchart;application/vnd.kde.kformula;application/vnd.kde.kivio;application/vnd.kde.kontour;application/vnd.kde.kpresenter;application/vnd.kde.kspread;application/vnd.kde.kword;application/vnd.kenameaapp;applicatin/vnd.kidspiration;application/vnd.kinar;application/vnd.kodak-descriptor;application/vnd.las.las+xml;application/x-latex;application/vnd.llamagraphics.life-balance.desktop;application/vnd.llamagraphics.life-balance.exchange+xml;application/vnd.jam;application/vnd.lotus-1-2-3;application/vnd.lotus-approach;application/vnd.lotus-freelance;application/vnd.lotus-notes;application/vnd.lotus-organizer;application/vnd.lotus-screencam;application/vnd.lotus-wordro;audio/vnd.lucent.voice;audio/x-mpegurl;video/x-m4v;application/mac-binhex40;application/vnd.macports.portpkg;application/vnd.osgeo.mapguide.package;application/marc;application/marcxml+xml;application/mxf;application/vnd.wolfrm.player;application/mathematica;application/mathml+xml;application/mbox;application/vnd.medcalcdata;application/mediaservercontrol+xml;application/vnd.mediastation.cdkey;application/vnd.mfer;application/vnd.mfmp;model/mesh;appliation/mads+xml;application/mets+xml;application/mods+xml;application/metalink4+xml;application/vnd.ms-powerpoint.template.macroenabled.12;application/vnd.ms-word.document.macroenabled.12;application/vnd.ms-word.template.macroenabed.12;application/vnd.mcd;application/vnd.micrografx.flo;application/vnd.micrografx.igx;application/vnd.eszigno3+xml;application/x-msaccess;video/x-ms-asf;application/x-msdownload;application/vnd.ms-artgalry;application/vnd.ms-ca-compressed;application/vnd.ms-ims;application/x-ms-application;application/x-msclip;image/vnd.ms-modi;application/vnd.ms-fontobject;application/vnd.ms-excel;application/vnd.ms-excel.addin.macroenabled.12;application/vnd.ms-excelsheet.binary.macroenabled.12;application/vnd.ms-excel.template.macroenabled.12;application/vnd.ms-excel.sheet.macroenabled.12;application/vnd.ms-htmlhelp;application/x-mscardfile;application/vnd.ms-lrm;application/x-msmediaview;aplication/x-msmoney;application/vnd.openxmlformats-officedocument.presentationml.presentation;application/vnd.openxmlformats-officedocument.presentationml.slide;application/vnd.openxmlformats-officedocument.presentationml.slideshw;application/vnd.openxmlformats-officedocument.presentationml.template;application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;application/vnd.openxmlformats-officedocument.spreadsheetml.template;application/vnd.openxmformats-officedocument.wordprocessingml.document;application/vnd.openxmlformats-officedocument.wordprocessingml.template;application/x-msbinder;application/vnd.ms-officetheme;application/onenote;audio/vnd.ms-playready.media.pya;vdeo/vnd.ms-playready.media.pyv;application/vnd.ms-powerpoint;application/vnd.ms-powerpoint.addin.macroenabled.12;application/vnd.ms-powerpoint.slide.macroenabled.12;application/vnd.ms-powerpoint.presentation.macroenabled.12;appliation/vnd.ms-powerpoint.slideshow.macroenabled.12;application/vnd.ms-project;application/x-mspublisher;application/x-msschedule;application/x-silverlight-app;application/vnd.ms-pki.stl;application/vnd.ms-pki.seccat;application/vn.visio;video/x-ms-wm;audio/x-ms-wma;audio/x-ms-wax;video/x-ms-wmx;application/x-ms-wmd;application/vnd.ms-wpl;application/x-ms-wmz;video/x-ms-wmv;video/x-ms-wvx;application/x-msmetafile;application/x-msterminal;application/msword;application/x-mswrite;application/vnd.ms-works;application/x-ms-xbap;application/vnd.ms-xpsdocument;audio/midi;application/vnd.ibm.minipay;application/vnd.ibm.modcap;application/vnd.jcp.javame.midlet-rms;application/vnd.tmobile-ivetv;application/x-mobipocket-ebook;application/vnd.mobius.mbk;application/vnd.mobius.dis;application/vnd.mobius.plc;application/vnd.mobius.mqy;application/vnd.mobius.msl;application/vnd.mobius.txf;application/vnd.mobius.daf;tex/vnd.fly;application/vnd.mophun.certificate;application/vnd.mophun.application;video/mj2;audio/mpeg;video/vnd.mpegurl;video/mpeg;application/mp21;audio/mp4;video/mp4;application/mp4;application/vnd.apple.mpegurl;application/vnd.msician;application/vnd.muvee.style;application/xv+xml;application/vnd.nokia.n-gage.data;application/vnd.nokia.n-gage.symbian.install;application/x-dtbncx+xml;application/x-netcdf;application/vnd.neurolanguage.nlu;application/vnd.na;application/vnd.noblenet-directory;application/vnd.noblenet-sealer;application/vnd.noblenet-web;application/vnd.nokia.radio-preset;application/vnd.nokia.radio-presets;text/n3;application/vnd.novadigm.edm;application/vnd.novadim.edx;application/vnd.novadigm.ext;application/vnd.flographit;audio/vnd.nuera.ecelp4800;audio/vnd.nuera.ecelp7470;audio/vnd.nuera.ecelp9600;application/oda;application/ogg;audio/ogg;video/ogg;application/vnd.oma.dd2+xml;applicatin/vnd.oasis.opendocument.text-web;application/oebps-package+xml;application/vnd.intu.qbo;application/vnd.openofficeorg.extension;application/vnd.yamaha.openscoreformat;audio/webm;video/webm;application/vnd.oasis.opendocument.char;application/vnd.oasis.opendocument.chart-template;application/vnd.oasis.opendocument.database;application/vnd.oasis.opendocument.formula;application/vnd.oasis.opendocument.formula-template;application/vnd.oasis.opendocument.grapics;application/vnd.oasis.opendocument.graphics-template;application/vnd.oasis.opendocument.image;application/vnd.oasis.opendocument.image-template;application/vnd.oasis.opendocument.presentation;application/vnd.oasis.opendocumen.presentation-template;application/vnd.oasis.opendocument.spreadsheet;application/vnd.oasis.opendocument.spreadsheet-template;application/vnd.oasis.opendocument.text;application/vnd.oasis.opendocument.text-master;application/vnd.asis.opendocument.text-template;image/ktx;application/vnd.sun.xml.calc;application/vnd.sun.xml.calc.template;application/vnd.sun.xml.draw;application/vnd.sun.xml.draw.template;application/vnd.sun.xml.impress;application/vnd.sun.xl.impress.template;application/vnd.sun.xml.math;application/vnd.sun.xml.writer;application/vnd.sun.xml.writer.global;application/vnd.sun.xml.writer.template;application/x-font-otf;application/vnd.yamaha.openscoreformat.osfpvg+xml;application/vnd.osgi.dp;application/vnd.palm;text/x-pascal;application/vnd.pawaafile;application/vnd.hp-pclxl;application/vnd.picsel;image/x-pcx;image/vnd.adobe.photoshop;application/pics-rules;image/x-pict;application/x-chat;aplication/pkcs10;application/x-pkcs12;application/pkcs7-mime;application/pkcs7-signature;application/x-pkcs7-certreqresp;application/x-pkcs7-certificates;application/pkcs8;application/vnd.pocketlearn;image/x-portable-anymap;image/-portable-bitmap;application/x-font-pcf;application/font-tdpfr;application/x-chess-pgn;image/x-portable-graymap;image/png;image/x-portable-pixmap;application/pskc+xml;application/vnd.ctc-posml;application/postscript;application/xfont-type1;application/vnd.powerbuilder6;application/pgp-encrypted;application/pgp-signature;application/vnd.previewsystems.box;application/vnd.pvi.ptid1;application/pls+xml;application/vnd.pg.format;application/vnd.pg.osasli;tex/prs.lines.tag;application/x-font-linux-psf;application/vnd.publishare-delta-tree;application/vnd.pmi.widget;application/vnd.quark.quarkxpress;application/vnd.epson.esf;application/vnd.epson.msf;application/vnd.epson.ssf;applicaton/vnd.epson.quickanime;application/vnd.intu.qfx;video/quicktime;application/x-rar-compressed;audio/x-pn-realaudio;audio/x-pn-realaudio-plugin;application/rsd+xml;application/vnd.rn-realmedia;application/vnd.realvnc.bed;applicatin/vnd.recordare.musicxml;application/vnd.recordare.musicxml+xml;application/relax-ng-compact-syntax;application/vnd.data-vision.rdz;application/rdf+xml;application/vnd.cloanto.rp9;application/vnd.jisp;application/rtf;text/richtex;application/vnd.route66.link66+xml;application/rss+xml;application/shf+xml;application/vnd.sailingtracker.track;image/svg+xml;application/vnd.sus-calendar;application/sru+xml;application/set-payment-initiation;application/set-reistration-initiation;application/vnd.sema;application/vnd.semd;application/vnd.semf;application/vnd.seemail;application/x-font-snf;application/scvp-vp-request;application/scvp-vp-response;application/scvp-cv-request;application/svp-cv-response;application/sdp;text/x-setext;video/x-sgi-movie;application/vnd.shana.informed.formdata;application/vnd.shana.informed.formtemplate;application/vnd.shana.informed.interchange;application/vnd.shana.informed.package;application/thraud+xml;application/x-shar;image/x-rgb;application/vnd.epson.salt;application/vnd.accpac.simply.aso;application/vnd.accpac.simply.imp;application/vnd.simtech-mindmapper;application/vnd.commonspace;application/vnd.ymaha.smaf-audio;application/vnd.smaf;application/vnd.yamaha.smaf-phrase;application/vnd.smart.teacher;application/vnd.svd;application/sparql-query;application/sparql-results+xml;application/srgs;application/srgs+xml;application/sml+xml;application/vnd.koan;text/sgml;application/vnd.stardivision.calc;application/vnd.stardivision.draw;application/vnd.stardivision.impress;application/vnd.stardivision.math;application/vnd.stardivision.writer;application/vnd.tardivision.writer-global;application/vnd.stepmania.stepchart;application/x-stuffit;application/x-stuffitx;application/vnd.solent.sdkm+xml;application/vnd.olpc-sugar;audio/basic;application/vnd.wqd;application/vnd.symbian.install;application/smil+xml;application/vnd.syncml+xml;application/vnd.syncml.dm+wbxml;application/vnd.syncml.dm+xml;application/x-sv4cpio;application/x-sv4crc;application/sbml+xml;text/tab-separated-values;image/tiff;application/vnd.to.intent-module-archive;application/x-tar;application/x-tcl;application/x-tex;application/x-tex-tfm;application/tei+xml;text/plain;application/vnd.spotfire.dxp;application/vnd.spotfire.sfs;application/timestamped-data;applicationvnd.trid.tpt;application/vnd.triscape.mxs;text/troff;application/vnd.trueapp;application/x-font-ttf;text/turtle;application/vnd.umajin;application/vnd.uoml+xml;application/vnd.unity;application/vnd.ufdl;text/uri-list;application/nd.uiq.theme;application/x-ustar;text/x-uuencode;text/x-vcalendar;text/x-vcard;application/x-cdlink;application/vnd.vsf;model/vrml;application/vnd.vcx;model/vnd.mts;model/vnd.vtu;application/vnd.visionary;video/vnd.vivo;applicatin/ccxml+xml,;application/voicexml+xml;application/x-wais-source;application/vnd.wap.wbxml;image/vnd.wap.wbmp;audio/x-wav;application/davmount+xml;application/x-font-woff;application/wspolicy+xml;image/webp;application/vnd.webturb;application/widget;application/winhlp;text/vnd.wap.wml;text/vnd.wap.wmlscript;application/vnd.wap.wmlscriptc;application/vnd.wordperfect;application/vnd.wt.stf;application/wsdl+xml;image/x-xbitmap;image/x-xpixmap;image/x-xwindowump;application/x-x509-ca-cert;application/x-xfig;application/xhtml+xml;application/xml;application/xcap-diff+xml;application/xenc+xml;application/patch-ops-error+xml;application/resource-lists+xml;application/rls-services+xml;aplication/resource-lists-diff+xml;application/xslt+xml;application/xop+xml;application/x-xpinstall;application/xspf+xml;application/vnd.mozilla.xul+xml;chemical/x-xyz;text/yaml;application/yang;application/yin+xml;application/vnd.ul;application/zip;application/vnd.handheld-entertainment+xml;application/vnd.zzazz.deck+xml")
            # turn off the spellcheck/autocomplete nonsense
            options.set_preference("layout.spellcheckDefault", 0)
            options.set_preference("dom.forms.autocomplete.formautofill", False)
            if headless:
                options.add_argument("--headless")
            self.__configure_common_options(options)
            self._driver = webdriver.Firefox(options=options, service=FirefoxService(GeckoDriverManager().install()))
            self.__scroll_button_offset = 18
        elif browser_type == BrowserType.EDGE:
            raise ValueError("We don't support Edge right now with this framework.. Sorry.")
        else:
            raise ValueError("Invalid browser type " + str(browser_type))
        self._driver.get(url)

    @staticmethod
    def x_path_ci_contains(search: str) -> str:
        """
        Returns part of XPath query that searches the element's text for the given string, case insensitively.
        :param search: element text
        :return: x-path query
        """
        return "[contains(translate(text(), \"abcdefghijklmnopqrstuvwxyz\", \"ABCDEFGHIJKLMNOPQRSTUVWXYZ\"), \"" + \
            search.upper() + "\")]"

    @staticmethod
    def x_path_ci_text_equals(search: str) -> str:
        """
        Returns part of XPath query that checks the element's text is equal to the given string, case insensitively.
        :param search: element text to search equality for
        :return: x-path query
        """
        return "[translate(normalize-space(text()), \"abcdefghijklmnopqrstuvwxyz\", " \
               "\"ABCDEFGHIJKLMNOPQRSTUVWXYZ\")=\"" + search.upper() + "\"]"

    @staticmethod
    def x_path_contains_class(class_name: str) -> str:
        """
        Returns part of an XPath query that checks if element this is appended to contains the given class name.
        :param class_name: the class name to search for
        :return: x-path query
        """
        return "[contains(concat(' ', normalize-space(@class), ' '), ' " + class_name + " ')]"

    @staticmethod
    def x_path_any_tag_of(tags: List[str]) -> str:
        if len(tags) == 1:
            return tags[0]
        query_list = ['local-name() = "' + tag + '"' for tag in tags]
        query = "*[" + " or ".join(query_list) + "]"
        return query

    def get_scroll_left(self, el: WebElement) -> int:
        """
        Get the position of the scrollbar position.
        :param el: The web element to query
        :return The relative position of left side. The result will be 0 if it's on the further left.
        """
        return int(self._driver.execute_script("return arguments[0].scrollLeft", el))

    def at_max_scroll_left(self, el: WebElement) -> bool:
        """
        Tests whether we are currently on furthest left of a scrolling view.
        """
        return self.get_scroll_left(el) == 0

    def at_max_scroll_right(self, el: WebElement) -> bool:
        """
        Tests whether we are currently on the furthest right of a scrolling view.
        """
        return self.get_scroll_left(el) + self.get_offset_width(el) >= self.get_scroll_width(el)

    def get_scroll_top(self, el: WebElement) -> int:
        """
        Get the position of the scrollbar top position
        :param el: The web element to query
        :return: The relative position of top side. The result will be 0 if it's on the furthest top.
        """
        return int(self._driver.execute_script("return arguments[0].scrollTop", el))

    def at_max_scroll_top(self, el: WebElement) -> bool:
        """
        Tests whether we are currently on furthest top of a scrolling view.
        :param el: The web element to query.
        """
        return self.get_scroll_top(el) == 0

    def at_max_scroll_bottom(self, el: WebElement) -> bool:
        """
        Tests whether we are currently on the furthest bottom of a scrolling view.
        :param el: The web element to query.
        """
        return self.get_scroll_top(el) + self.get_offset_height(el) >= self.get_scroll_height(el)

    def get_scroll_width(self, el: WebElement) -> int:
        """
        Get the width of the entire scrolling view (that spans multiple pages).
        :param el: The web element to query.
        :return: The total width of the scrolling element.
        """
        return int(self._driver.execute_script("return arguments[0].scrollWidth", el))

    def get_scroll_height(self, el: WebElement) -> int:
        """
        Get the height of the entire scrolling view (that spans multiple pages).
        :param el: The web element to query.
        :return: The total height of the scrolling element.
        """
        return int(self._driver.execute_script("return arguments[0].scrollHeight", el))

    def get_offset_width(self, el: WebElement) -> int:
        """
        Get the offset width of a web element.
        :param el: The web element to query.
        :return: The total width of the element.
        """
        return int(self._driver.execute_script("return arguments[0].offsetWidth", el))

    def get_offset_height(self, el: WebElement) -> int:
        """
        Get the offset height of a web element
        :param el: The web element to query
        :return: The total offset height of the element.
        """
        return int(self._driver.execute_script("return arguments[0].offsetHeight", el))

    def get_inner_text(self, el: WebElement) -> str:
        """
        Get the containing text of a web element.
        :param el: The web element to query
        :return: The inner text of the element selected.
        """
        return str(self._driver.execute_script("return arguments[0].innerText", el))

    def is_element_under_pointer(self, el: WebElement) -> bool:
        """
        Tests whether the element is currently on my cursor hover.
        :param el: the web element to be tested now.
        """
        try:
            script = """
            var hoverEls = document.querySelectorAll(':hover');
            if (hoverEls == null) { return false; }
            var el = arguments[0];
            var hoverEl = hoverEls.item(hoverEls.length-1);
            while (hoverEl != el && hoverEl.parentNode != null) {
                hoverEl = hoverEl.parentNode
            }
            return hoverEl == el
            """
            return bool(self._driver.execute_script(script, el))
        except Exception as e:
            return False

    def scroll_to_left(self, el: WebElement) -> None:
        """
        Perform one operation of attempting to scroll to the left.
        :param el: The web element to scroll.
        """
        if self.at_max_scroll_left(el) == 0:
            return
        size = el.size
        width = size["width"]
        height = size["height"]
        actions = ActionChains(self._driver) \
            .move_to_element_with_offset(el, width / -2 + self.__scroll_button_offset, height / 2 - 6) \
            .click()
        actions.perform()

    def scroll_to_right(self, el: WebElement) -> None:
        """
        Perform one operation of attempting to scroll to the right.
        :param el: The element to scroll
        """
        if self.at_max_scroll_right(el):
            return
        size = el.size
        width = size["width"]
        height = size["height"]
        actions = ActionChains(self._driver) \
            .move_to_element_with_offset(el, width / 2 - self.__scroll_button_offset, height / 2 - 6) \
            .click()
        actions.perform()

    def scroll_up(self, el: WebElement, force: bool = False) -> None:
        """
        Perform once-time scroll up.
        :param el: The web element to scroll.
        :param force: perform scrolling even if we are already at the top position.
        """
        if not force and self.at_max_scroll_top(el):
            return
        size = el.size
        width = size["width"]
        height = size["height"]
        self._driver.execute_script("arguments[0].scrollBy(0, -" + str(height // 2) + ")", el)
        # scroll_offset = 0
        # if self._browser_type == BrowserType.FIREFOX:
        #     scroll_offset = self.__scroll_button_offset
        # actions = ActionChains(self._driver) \
        #     .move_to_element_with_offset(el, width / 2 - 6, height / -2 + scroll_offset) \
        #     .click()
        # actions.perform()

    def scroll_down(self, el: WebElement, force: bool = False) -> None:
        """
        Performce once-time scroll down.
        :param el: The web element to scroll
        :param force: perform scrolling even if we are already at the bottom position.
        """
        if not force and self.at_max_scroll_bottom(el):
            return
        size = el.size
        width = int(size["width"])
        height = int(size["height"])
        """
        if this is an ELN entry, we have an issue where the very bottom of the scrollbar is actually not clickable
        since the resize handler for the entry will eat the event.
        Would be easiest to just come up a few pixels in that case, but this causes issues when there are horizontal 
        scrollbars, as well.
        Solution: hover over the very bottom and then see if the scrollbar element is the element under the cursor.
        If it is, then we click.  Otherwise, we come up a few pixels and go for broke.
        """
        self._driver.execute_script("arguments[0].scrollBy(0, " + str(height // 2) + ")", el)
        # actions = ActionChains(self._driver).move_to_element_with_offset(el, width // 2 - 6, height // 2 - 1)
        # actions.perform()
        # if self._browser_type != BrowserType.FIREFOX and self.is_element_under_pointer(el):
        #     ActionChains(self._driver).click().perform()
        # else:
        #     ActionChains(self._driver) \
        #         .move_to_element_with_offset(el, width // 2 - 6, height // 2 - self.__scroll_button_offset) \
        #         .click().perform()

    def scroll_to_far_left(self, el: WebElement, max_tries: int = 100) -> None:
        """
        Perform scrolling operation to scroll to far left side in this web element.
        :param el: The element to scroll.
        :param max_tries Maximum number of scrolling left attempts
        """
        i = 0
        while i < max_tries and not self.at_max_scroll_left(el):
            self.scroll_to_left(el)
            i += 1

    def scroll_to_far_right(self, el: WebElement, max_tries: int = 100) -> None:
        """
        Keep scrolling to the right until we hit the rightmost part of the view.
        :param el: The element to scroll
        :param max_tries: Maximum number of scrolling right attempts.
        """
        i = 0
        while i < max_tries and not self.at_max_scroll_right(el):
            self.scroll_to_right(el)
            i += 1

    def scroll_to_very_top(self, el: WebElement, max_tries=200) -> None:
        """
        Keep scrolling to the top until we hit the top most part of the view.
        :param el: The element to scroll up.
        :param max_tries: Maximum number of scrolling top attempts.
        """
        i = 0
        while i < max_tries and not self.at_max_scroll_top(el):
            self.scroll_up(el)
            i += 1

    def scroll_to_very_bottom(self, el: WebElement, max_tries=200) -> None:
        """
        Keep scrolling to the bottom until we hit the bottom most part of the view.
        :param el: The element to scroll bottom.
        :param max_tries: Maximum number of scrolling bottom attempts.
        """
        i = 0
        while i < max_tries and not self.at_max_scroll_bottom(el):
            self.scroll_down(el)
            i += 1

    def take_screenshot(self, file_name: str) -> bool:
        """
        Take a screenshot of current window and save as a file.
        :param file_name: The PNG file path to be saving the screenshot. Must be absolute.
        :return: Returns False if error. Returns true if screenshot was saved.
        """
        file_name = file_name + ".png"
        return self._driver.get_screenshot_as_file(os.path.join(self.file_man.screenshot_dir, file_name))

    def focus(self, el: WebElement) -> None:
        self._driver.execute_script("arguments[0].focus", el)

    def scroll_into_view(self, el: WebElement, align_to_top=True) -> None:
        """
        Scroll element into view of the parent container
        :param el: Element target to scroll to become visible.
        :param align_to_top: If true (default), top of the element will be aligned to visible area.
        If false, bottom of the element will be aligned to visible area.
        """
        self._driver.execute_script("arguments[0].scrollIntoView(" + str(align_to_top).lower() + ");", el)

    def wait_for(self, element_finder: Callable[[WebDriver], Optional[WebElement]],
                 timeout_seconds: float = 60, must_be_visible: bool = True) -> WebElement:
        """
        Wait for appearance of a specific web element to be findable.
        :param element_finder: The function that finds a web element
        :param timeout_seconds The number of seconds to wait for.
        :param must_be_visible: Whether the element must be visible or displayed before returning element.
        """
        final_finder: Callable[[WebDriver], Optional[WebElement]]
        if not must_be_visible:
            final_finder = element_finder
        else:
            def finder(driver: WebDriver) -> Optional[WebElement]:
                el: Optional[WebElement] = element_finder(driver)
                if not el:
                    return None
                if must_be_visible and not el.is_displayed():
                    return None
                return el

            final_finder = finder
        return self.wait(timeout_seconds).until(final_finder)

    def wait_for_many(self, element_finders: Callable[[WebDriver], Optional[List[WebElement]]],
                      timeout_seconds: float = 60) -> List[WebElement]:
        """
        Wait until a list of elements exists in the web widgets, up to a timeout.
        :param element_finders: A function that finds elements in web widgets.
        :param timeout_seconds: The maximum waits in seconds.
        """

        def final_finder(driver: WebDriver) -> Optional[List[WebElement]]:
            results: Optional[List[WebElement]] = element_finders(driver)
            if not results:
                return None
            return results

        return self.wait(timeout_seconds).until(final_finder)

    def is_visible_in_viewport(self, el: WebElement):
        """
        Determines if the center of the element is within the browser viewport.
        Would also return false if there is an element on top of (z-index) the given element.
        via: https://stackoverflow.com/a/45244889
        :param el: The element to check
        :return: true iff the element is visible to user right now in this viewport (if taking screenshot now)
        """
        script = """
        var elem = arguments[0], box = elem.getBoundingClientRect(), cx = box.left + box.width / 2,
        cy = box.top + box.height / 2, e = document.elementFromPoint(cx, cy);
        for (; e; e = e.parentElement) {
            if (e === elem){
                return true;
            }
        }
        return false;
        """
        return bool(self._driver.execute_script(script, el))

    def wait_until_clickable(self, element_finder: Callable[[WebDriver], Optional[WebElement]],
                             timeout_seconds: float = 60) -> Optional[WebElement]:
        """
        Wait until the element is rendered in the current view port, and with no obstruction.
        :param element_finder: The query function to find element.
        :param timeout_seconds: Maximum wait timeout in seconds.
        """

        def final_finder(driver: WebDriver) -> Optional[WebElement]:
            el: WebElement = element_finder(driver)
            if el.is_displayed() and self.is_visible_in_viewport(el):
                return el
            return None

        return self.wait(timeout_seconds).until(final_finder)

    def click(self, el: WebElement, timeout_seconds: float = 60) -> Optional[WebElement]:
        """
        Wait until the element is clickable before clicking the element.
        """

        def do_click(d: WebDriver) -> WebElement:
            self.handle_toastr_click()
            el.click()
            return el

        ret: WebElement = self.wait(timeout_seconds=timeout_seconds,
                                    ignored_exceptions=[NoSuchElementException, ElementClickInterceptedException]
                                    ).until(do_click)
        return ret

    def drop_file(self, file_path: Path, target: WebElement, timeout_seconds: float = 60) -> None:
        """
        Simulates a drag and drop of a file onto a drop target.
        """
        if not file_path.exists():
            raise IOError("File not found: " + str(file_path))
        script = """
        var target = arguments[0], document = target.ownerDocument || document, window = document.defaultView || window;
        var input = document.createElement('INPUT');
        input.type = 'file';
        input.style.display = 'none';
        input.onchange = function () {
            var rect = target.getBoundingClientRect(),x = rect.left + (rect.width / 2),y = rect.top + (rect.height / 2),
            dataTransfer = { files: this.files };
            var timeout = 250;
            ['dragenter', 'dragover1', 'dragover2', 'drop', 'done'].forEach(function (name) {
                setTimeout(function() {
                    if (name === 'done') {
                        document.body.removeChild(input);
                        return;
                    }
                    var evt = document.createEvent('MouseEvent');
                    var xx = x, yy = y;
                    if (name === 'dragenter' || name === 'dragover1') {
                        xx = 1, yy = 1;
                    }
                    if (name.indexOf('dragover') === 0) {
                        name = 'dragover';
                    }
                    evt.initMouseEvent(name, !0, !0, window, 0, 0, 0, xx, yy, !1, !1, !1, !1, 0, null);
                    evt.dataTransfer = dataTransfer;
                    document.elementFromPoint(xx,yy).dispatchEvent(evt);
                }, timeout);
                timeout += 250;
            });
        };
        document.body.appendChild(input);
        return input;
        """
        web_input: WebElement = self._driver.execute_script(script, target)
        web_input.send_keys(str(file_path.absolute()))
        self.wait(timeout_seconds).until(staleness_of(web_input))

    def get_element_at_point(self, x: int, y: int) -> WebElement:
        return self._driver.execute_script("return document.elementFromPoint(arguments[0], arguments[1]);", x, y)

    def stale_wait(self, timeout_seconds=10, additional_ignores: List[Type] = None) -> WebDriverWait:
        """
        Returns a new wait object with timeout duration that will ignore stale element exceptions.
        :param timeout_seconds: timeouts maximum to wait for staleness.
        """
        ignored_exceptions = [StaleElementReferenceException]
        if additional_ignores:
            ignored_exceptions.extend(additional_ignores)
        return WebDriverWait(self._driver, timeout_seconds, ignored_exceptions=ignored_exceptions)

    def wait_until_refreshed(self, supplier: Callable[[WebDriver], Any], timeout_seconds=10) -> Any:
        return self.wait(timeout_seconds).until(supplier)

    def get_style_property(self, el: WebElement, prop: str) -> Optional[str]:
        """
        Gets the value of the specified property off of the element's style attribute.
        Don't use dashes in property names.
        """
        return self._driver.execute_script("return arguments[0].style[arguments[1]];", el, prop)

    def is_stale(self, el: WebElement) -> bool:
        call: Callable[[AnyDriver], bool] = staleness_of(el)
        return call(self._driver)

    def exists(self, by: By, query_by: str, timeout_seconds: Optional[float] = None,
               visible_required: bool = False) -> bool:
        """
        Whether the element can be found.
        """
        return self.exists_by_supplier(lambda d: self._driver.find_element(by, query_by),
                                       timeout_seconds, visible_required)

    def exists_in_element(self, parent_element: WebElement, by: By, query_by: str,
                          timeout_seconds: Optional[float] = None, visible_required: bool = False):
        """
        Check whether the element can be found inside a parent element.
        """
        return self.exists_by_supplier(lambda d: parent_element.find_element(by, query_by),
                                       timeout_seconds, visible_required)

    def exists_by_supplier(self, method: Callable[[WebDriver], WebElement], timeout_seconds: Optional[float] = None,
                           visible_required: bool = False) -> bool:
        """
        Whether the supplier method returns non-null, visible web element.
        """
        found: bool = False

        if timeout_seconds is not None:
            sleep(timeout_seconds)
        # noinspection PyBroadException
        try:
            el = method(self._driver)
            if el:
                found = True
                if visible_required:
                    found = self.is_visible_in_viewport(el)
        except Exception as e:
            pass

        return found

    @staticmethod
    def normalize_text(text: str) -> str:
        """
        The text for buttons typically has newline characters in it.  This method cleans up such value so that they can
        be more easily compared.  Should pass the button text and the given search text through this method before
        comparing.
        """
        if not text:
            return ""
        text = text.upper()
        return re.sub("\\s+", " ", text).strip()

    def send_keys(self, keys: str, ele: Optional[WebElement] = None):
        """
        Send a list of key presses, either onto an element or the entire document.
        For special keys use Keys class constants.
        """
        if not ele:
            actions = ActionChains(self._driver)
            for k in keys_to_typing(keys):
                actions.key_down(k, ele)
                actions.key_up(k, ele)
                # firefox driver currently has issue typing things out of order :(
                if self.browser_type == BrowserType.FIREFOX:
                    actions.pause(.3)
            actions.perform()
        else:
            ele.send_keys(keys)

    @staticmethod
    def wait_seconds(seconds: float) -> None:
        """
        Delay execution by specified seconds.
        """
        sleep(seconds)

    @staticmethod
    def __configure_common_options(options):
        options.accept_insecure_certs = True

    def wait(self, timeout_seconds: float = 60, ignored_exceptions=None):
        """
        Standard wait object construction handling typical web loading cases.
        """
        if ignored_exceptions is None:
            ignored_exceptions = [NoSuchElementException]
        return WebDriverWait(self._driver, timeout_seconds,
                             ignored_exceptions=ignored_exceptions)

    def wait_until_presence_of_element_under_xpath(self, parent_element: WebElement, by: str, query: str) -> WebElement:
        """
        This is to work around the relative pathing not supported by EC directly.
        We wait until the element exists in the DOM.
        """
        return self.wait().until(parent_element.find_element(by, query))

    def wait_until_element_visible(self, parent_element: WebElement, by: str, query: str,
                                   timeout_seconds: float = 60) -> WebElement:
        """
        This is to work around the relative pathing not supported by EC directly.
        We wait until the element is displayed right now. (i.e. has height, width > 0 and not hidden)
        """

        def supplier(d: WebDriver) -> Optional[WebElement]:
            element = parent_element.find_element(by, query)
            if element is None:
                return None
            if not element.is_displayed():
                return None
            return element

        return self.wait(timeout_seconds).until(supplier)

    # noinspection PyBroadException
    def handle_toastr_click(self):
        """
        If toastr had appeared, click the toastr.
        If toastr doesn't exist or naturally went away, don't blow up.
        """
        try:
            ele: WebElement = self._driver.find_element(By.XPATH, TOASTR_XPATH)
            ele.click()
        except Exception as e:
            pass


