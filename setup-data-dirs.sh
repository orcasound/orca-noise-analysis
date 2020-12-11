# setup-data-dirs.sh
#
# Set up data directory structure in the local root directory
# (explicitly not in the repository, to avoid hitting the 100MB Github limit)
# for temporary storage of audio and ais data during processing
#

# Should eventually add some logic to ensure there isn't any data/strucutre that gets overwritten!

mkdir ~/shipnoise-data
mkdir ~/shipnoise-data/audio
mkdir ~/shipnoise-data/audio/test
mkdir ~/shipnoise-data/ais
