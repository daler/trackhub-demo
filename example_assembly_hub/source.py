import trackhub
import re
import sys
import os
import glob

# In contrast to the example in the README, we do not use the
# `trackhub.default_hub` function but instead build up the hub from its
# component pieces.
hub = trackhub.Hub(
    "assembly_hub",
    short_label="assembly_hub",
    long_label="an example of an assembly hub",
    email="none@example.com")

# The major difference from a regular track hub is this object, which needs
# to be added to the genomes_file object:
genome = trackhub.Assembly(
    genome="newOrg1",
    twobit_file=os.path.join(trackhub.helpers.data_dir(), "newOrg1.2bit"),
    organism="Big Foot",
    defaultPos="chr1:0-1000000",
    scientificName="Biggus Footus",
    description="BigFoot V4",
    html_string="BIGFOOT V4 INFO\n",
    orderKey=4800
)

genomes_file = trackhub.GenomesFile()
hub.add_genomes_file(genomes_file)

# we also need to create a trackDb and add it to the genome
trackdb = trackhub.TrackDb()
genome.add_trackdb(trackdb)

# add the genome to the genomes file here:
genomes_file.add_genome(genome)

# Find all bigwigs for this genome in the example data directory, and make
# tracks for them
for bw in glob.glob(os.path.join(trackhub.helpers.data_dir(), "*no1*.bw")):
    name, _, _ = os.path.basename(bw).split(".")
    track = trackhub.Track(
        name=trackhub.helpers.sanitize(name),
        source=bw,
        tracktype='bigWig',
        autoScale='on')
    trackdb.add_tracks(track)

# Same with bigBeds
for bb in glob.glob(os.path.join(trackhub.helpers.data_dir(), "*no1*.bigBed")):
    name, _ = os.path.basename(bb).split(".")
    track = trackhub.Track(
        name=trackhub.helpers.sanitize(name),
        source=bb,
        tracktype='bigBed')
    trackdb.add_tracks(track)

# Assembly hubs also need to have a Group specified. Here's how to do that:
example_group = trackhub.groups.GroupDefinition(
    "example_tracks",
    label="Example Tracks",
    priority=1,
    default_is_closed=False)

groups_file = trackhub.groups.GroupsFile([example_group])
genome.add_groups(groups_file)

# We can now add the "group" parameter to all the children of the trackDb
for track in trackdb.children:
    track.add_params(group="example_tracks")

trackhub.upload.upload_hub(hub=hub, host='localhost',
    remote_dir='example_hubs/example_assembly_hub')