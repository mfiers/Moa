
epydoc -vo $MOABASE/doc/api \
    $MOABASE/bin/moa \
    $MOABASE/lib/python/moa/*py \
    -u http://mfiers.github.com/Moa/ \
    --name "Moa" --no-frames
