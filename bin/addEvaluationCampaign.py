#!/usr/bin/env python2

import optparse
import os
import sys

from corpus.models import EvaluationCampaign

optionParser = optparse.OptionParser(usage="%s [options] <name>" % os.environ["ESMT_PROG_NAME"], add_help_option=False)
optionParser.add_option("-h", "--help", action="help", help=optparse.SUPPRESS_HELP)
optionParser.add_option("-d", "--description", dest="description", help="description", default="", metavar="DESC")
(options, args) = optionParser.parse_args()

if len(args) == 0:
    optionParser.error("No campaign name given")
if len(args) > 1:
    optionParser.error("Only one campaign name can be given")

log = sys.stdout

foundCampaign = EvaluationCampaign.objects.filter(id=args[0])
if foundCampaign:
    sys.stderr.write("Error: campaign \"%s\" already exists in the database (as %s)\n" % (options.id))
else:
    c = EvaluationCampaign(args[0], description=options.description)
    c.save()
    log.write("Campaign %s added to the database\n" % c.id)
