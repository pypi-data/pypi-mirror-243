import logging
import sys

from sapioseleniumlib.script.truseq_dna import TruSeqDnaSequencingFromBlood
from sapioseleniumlib.util.driver import BrowserType
from testconfig import HOMEPAGE_URL, username, password

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logging.getLogger().setLevel(logging.INFO)

test = TruSeqDnaSequencingFromBlood(BrowserType.CHROME, HOMEPAGE_URL, username, password,
                                    False, run_id="TruSeqDNABlood",)
                                    # browser_binary_location="/usr/bin/firefox")
test.run()
