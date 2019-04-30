for i in {1..1};
do
 python cmotp.py --environment CMOTP_V3 --processor '/gpu:0' --madrl leniency
done
