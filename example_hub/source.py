import glob, os
import trackhub

# First we initialize the components of a track hub
hub, genomes_file, genome, trackdb = trackhub.default_hub(
    hub_name="myhub",
    short_label='myhub',
    long_label='myhub',
    genome="hg38",
    email="dalerr@niddk.nih.gov")

# Next, we add a track for every bigwig found.  In practice, you would
# point to your own files. In this example we use the path to the data
# included with trackhub.

for bigwig in glob.glob('trackhub/test/data/sine-hg38-*.bw'):
    name = trackhub.helpers.sanitize(os.path.basename(bigwig))
    track = trackhub.Track(
        name=name,          # track names can't have any spaces or special chars.
        source=bigwig,      # filename to build this track from
        visibility='full',  # shows the full signal
        color='128,0,5',    # brick red
        autoScale='on',     # allow the track to autoscale
        tracktype='bigWig', # required when making a track
    )

    # Each track is added to the trackdb
    trackdb.add_tracks(track)

# In this example we "upload" the hub locally. Files are created in the
# "example_hub" directory, along with symlinks to the tracks' data files.
# This directory can then be pushed to GitHub or rsynced to a server.
trackhub.upload.upload_hub(hub=hub, host='localhost', remote_dir='example_hubs/example_hub')

# Alternatively, we could upload directly to a web server (not run in this
# example):
if 0:
    trackhub.upload.upload_hub(
        hub=hub, host='example.com', user='username',
        remote_dir='/var/www/example_hub')