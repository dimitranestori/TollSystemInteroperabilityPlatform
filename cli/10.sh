python se2410.py healthcheck
python se2410.py resetpasses
python se2410.py healthcheck
python se2410.py resetstations
python se2410.py healthcheck
python se2410.py admin --addpasses --source passes10.csv
python se2410.py healthcheck
python se2410.py tollstationpasses --station AM08 --from 20220703 --to 20220717 --format json
python se2410.py tollstationpasses --station NAO04 --from 20220703 --to 20220717 --format csv
python se2410.py tollstationpasses --station NO01 --from 20220703 --to 20220717 --format csv
python se2410.py tollstationpasses --station OO03 --from 20220703 --to 20220717 --format csv
python se2410.py tollstationpasses --station XXX --from 20220703 --to 20220717 --format csv
python se2410.py tollstationpasses --station OO03 --from 20220703 --to 20220717 --format YYY
python se2410.py errorparam --station OO03 --from 20220703 --to 20220717 --format csv
python se2410.py tollstationpasses --station AM08 --from 20220704 --to 20220715 --format json
python se2410.py tollstationpasses --station NAO04 --from 20220704 --to 20220715 --format csv
python se2410.py tollstationpasses --station NO01 --from 20220704 --to 20220715 --format csv
python se2410.py tollstationpasses --station OO03 --from 20220704 --to 20220715 --format csv
python se2410.py tollstationpasses --station XXX --from 20220704 --to 20220715 --format csv
python se2410.py tollstationpasses --station OO03 --from 20220704 --to 20220715 --format YYY
python se2410.py passanalysis --stationop AM --tagop NAO --from 20220703 --to 20220717 --format json
python se2410.py passanalysis --stationop NAO --tagop AM --from 20220703 --to 20220717 --format csv
python se2410.py passanalysis --stationop NO --tagop OO --from 20220703 --to 20220717 --format csv
python se2410.py passanalysis --stationop OO --tagop KO --from 20220703 --to 20220717 --format csv
python se2410.py passanalysis --stationop XXX --tagop KO --from 20220703 --to 20220717 --format csv
python se2410.py passanalysis --stationop AM --tagop NAO --from 20220704 --to 20220715 --format json
python se2410.py passanalysis --stationop NAO --tagop AM --from 20220704 --to 20220715 --format csv
python se2410.py passanalysis --stationop NO --tagop OO --from 20220704 --to 20220715 --format csv
python se2410.py passanalysis --stationop OO --tagop KO --from 20220704 --to 20220715 --format csv
python se2410.py passanalysis --stationop XXX --tagop KO --from 20220704 --to 20220715 --format csv
python se2410.py passescost --stationop AM --tagop NAO --from 20220703 --to 20220717 --format json
python se2410.py passescost --stationop NAO --tagop AM --from 20220703 --to 20220717 --format csv
python se2410.py passescost --stationop NO --tagop OO --from 20220703 --to 20220717 --format csv
python se2410.py passescost --stationop OO --tagop KO --from 20220703 --to 20220717 --format csv
python se2410.py passescost --stationop XXX --tagop KO --from 20220703 --to 20220717 --format csv
python se2410.py passescost --stationop AM --tagop NAO --from 20220704 --to 20220715 --format json
python se2410.py passescost --stationop NAO --tagop AM --from 20220704 --to 20220715 --format csv
python se2410.py passescost --stationop NO --tagop OO --from 20220704 --to 20220715 --format csv
python se2410.py passescost --stationop OO --tagop KO --from 20220704 --to 20220715 --format csv
python se2410.py passescost --stationop XXX --tagop KO --from 20220704 --to 20220715 --format csv
python se2410.py chargesby --opid NAO --from 20220703 --to 20220717 --format json
python se2410.py chargesby --opid GE --from 20220703 --to 20220717 --format csv
python se2410.py chargesby --opid OO --from 20220703 --to 20220717 --format csv
python se2410.py chargesby --opid KO --from 20220703 --to 20220717 --format csv
python se2410.py chargesby --opid NO --from 20220703 --to 20220717 --format csv
python se2410.py chargesby --opid NAO --from 20220704 --to 20220715 --format json
python se2410.py chargesby --opid GE --from 20220704 --to 20220715 --format csv
python se2410.py chargesby --opid OO --from 20220704 --to 20220715 --format csv
python se2410.py chargesby --opid KO --from 20220704 --to 20220715 --format csv
python se2410.py chargesby --opid NO --from 20220704 --to 20220715 --format csv