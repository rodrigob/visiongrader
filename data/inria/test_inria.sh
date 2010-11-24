#!/bin/sh

# expected arguments:
newcurve=$1 # the eblearn bbox output file
dir=$2 # the directory containing other curves (pickle files)

vgdir=~/visiongrader/
#inria=/data/pedestrians/inria/INRIAPerson/Train/annotations/
inria=/data/pedestrians/inria/INRIAPerson/Test/annotations/
#inria=/data/pedestrians/inria/INRIAPerson/Test/tmpann/
inria_ignore=${vgdir}/data/inria/ignore/
#inria=/data/pedestrians/INRIAPerson/Test/annotations/
#inria=${hostname}adata/pedestrians/test/inria/
#inria=/data/pedestrians/inria_caltech/annotations/set01/V000.vbb
#gtparser=caltech #inria
gtparser=inria

# approximation of curve to avoid computing all possible thresholds
sampling="--sampling 50"
xmin=0.003
xmax=102
ymin=0.03
ymax=1.1
gt_whratio="--gt_whratio .43"
#whratio="--whratio .43"
#hratio="--hratio 1.145"
#wratio="--wratio 1.055"
#hratio="--hratio 1.01"
#whratio="--whratio .43"

ignore="--ignore $inria_ignore"
comp_threshold=.5
extract_caltech=0
show_caltech_db=0
show_caltech_db1= #HOG # show 1 caltech db
caltech=$vgdir/res/
# list of algorithms to resize
caltech_resize="HOG FtrMine Shapelet-orig PoseInv PoseInvSvm HikSvm"
caltech_hresize=`echo "scale=10;100.0 / 128.0" | bc`
echo "Resizing height ratio for certain caltech algorithms: ${caltech_hresize}"

################################################################################

if [ "${show_caltech_db1}" != "" ]
then
    algo=${show_caltech_db1}
    # check if algo needs to be resized
    resize_cmd=""
    echo $caltech_resize | grep $algo
    if [ $? -eq 0 ]
    then
	echo "Resizing algo ${algo}."
	resize_cmd="--hratio ${caltech_hresize} --whratio .43"
    fi
    python $vgdir/main.py --input $caltech/$algo/set01/V000 \
	--input_parser caltech \
	--groundtruth $inria --groundtruth_parser $gtparser --disp \
	$gt_whratio --images_path $inria \
	--comparator overlap50percent \
	--comparator_param ${comp_threshold} $ignore $resize_cmd
 fi

################################################################################
# generate caltech algos curves

test -d $caltech
if [ $? -eq 0 ] ; then
if [ $extract_caltech -eq 1 ] ; then
    for i in `ls -d $caltech/*/`; do
	algodir=$i/set01/V000/
	algo=`basename $i`
	echo "_________________________________________________________________"
	echo "Processing algorithm $algo"
	# check if algo needs to be resized
	resize_cmd=""
	echo $caltech_resize | grep $algo
	if [ $? -eq 0 ]
	then
	    echo "Resizing algo ${algo}."
	    resize_cmd="--hratio ${caltech_hresize} --whratio .43"
	fi
	python $vgdir/main.py --input $algodir --input_parser caltech \
    	    --groundtruth $inria  --groundtruth_parser $gtparser $gt_whratio \
    	    $sampling --xmin $xmin --xmax $xmax --ymin $ymin --ymax $ymax \
    	    --comparator overlap50percent \
	    --comparator_param ${comp_threshold} \
	    --det --saving-file $dir/$algo.pickle \
    	    --show-no-curve --confidence_min -5 $ignore $resize_cmd $whratio
	if [ $? -ne 0 ] ; then
	    echo "Error, stopping."
	    exit -1
	fi
	if [ $show_caltech_db -eq 1 ] ; then
            # show db
	    echo "_____________________________________________________________"
	    echo "Showing images for algo ${algodir}"
	    python $vgdir/main.py --input $algodir --input_parser caltech \
		--groundtruth $inria --groundtruth_parser $gtparser --disp \
		$gt_whratio --images_path $inria \
		--comparator overlap50percent \
		--comparator_param ${comp_threshold} $ignore $resize_cmd
	fi
    done
fi
fi

################################################################################

# generate curves for inria dataset using visiongrader project
# $1 should be the bounding box output file
python $vgdir/main.py --input $newcurve --input_parser eblearn \
    --groundtruth $inria  --groundtruth_parser $gtparser \
    $ignore $gt_whratio $whratio $hratio $wratio \
    $sampling --xmin $xmin --xmax $xmax --ymin $ymin --ymax $ymax \
    --comparator overlap50percent --comparator_param ${comp_threshold} \
    --det --saving-file $newcurve.pickle \
    --show-no-curve

# plot
python $vgdir/plotpickle.py --main_curve $newcurve.pickle \
    --xmin $xmin --xmax $xmax --ymin $ymin --ymax $ymax $dir/*.pickle  \
    --xlegend "False positives per image" --ylegend "Miss rate" \
    --grid_major --grid_minor

# show db
python $vgdir/main.py --input $newcurve --input_parser eblearn --disp \
    --groundtruth $inria --groundtruth_parser inria \
    $ignore $gt_whratio $whratio $hratio $wratio \
    --images_path $inria \
    --comparator overlap50percent --comparator_param ${comp_threshold}
    

################################################################################