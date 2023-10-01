if [ ! -d magenta ]
then
    echo GATHERING MAGENTA-GANSYNTH
    git clone https://github.com/peregoniccolo/magenta.git

    echo GATHERING SAMPLE MIDI FILES
    mkdir magenta/midi
    curl -o magenta/midi/bach.mid http://www.jsbach.net/midi/cs1-1pre.mid
    curl -o magenta/midi/riff-default.mid http://storage.googleapis.com/magentadata/papers/gansynth/midi/arp.mid
fi

if [ ! -d Music-Visualizer ]
then
    echo GATHERING MUSIC-VISUALIZER
    git clone https://github.com/peregoniccolo/Music-Visualizer
fi

if [ ! -d style-transfer-video-processor ]
then
    echo GATHERING STYLE-TRANSFER-VIDEO-PROCESSOR
    git clone https://github.com/peregoniccolo/style-transfer-video-processor
fi

if [ ! -d real-time-style-transfer ]
then
    echo GATHERING REAL-TIME-STYLE-TRANSFER
    git clone https://github.com/peregoniccolo/real-time-style-transfer
fi

echo ALL DONE