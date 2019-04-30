for i in {1..10};
do
 python main.py --environment CMOTP_V3 --processor '/gpu:0' --madrl leniency
done
