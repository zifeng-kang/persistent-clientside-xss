start_line=$1
end_line=$2
if_flush=$3 # 1 for flush in path TAG="", 0 for flush in path TAG="...", other for not flush
#sleep_time=$4
max_num_window=$4

rm -rf ~/.cache/chromium
if ((if_flush == 1))
then
        rm -rf ../crawl && mkdir ../crawl
        rm -rf logs && mkdir logs
        TAG=""
else
        TAG="p_"
        if ((if_flush == 0))
        then
                # rm -rf ../${TAG}crawl && mkdir ../${TAG}crawl
                rm -rf ${TAG}logs
                mkdir ${TAG}logs
        else
                mkdir ${TAG}logs
                # mkdir ../${TAG}crawl
        fi

fi

while IFS=, read -r idx url
do
    if (( idx > $start_line && idx <= $end_line ))
    then
            url="${url//[$'\t\r\n ']}" #remove newline from string
            NAME="${url/./_}"
            echo "${idx} ${url} ${TAG}logs/${NAME}_log_file sanchecker/${TAG}crawl/$NAME"
            # user /tmp/1 already has the minimal extension installed
            ./chrome ${url} --no-sandbox --disable-xss-auditor --disable-improved-download-protection --js-flags='--noblock_tainted' --user-data-dir=/tmp/1 \
                --new-window --enable-logging=stderr --v=1 > ${TAG}logs/${NAME}_log_file 2>&1 &

            # out/Bytecode/chrome ${url}/\#INJECT --js-flags="--taint_log_file=/media/data1/zfk/Documents/sanchecker/${TAG}crawl/$NAME --no-crankshaft --no-turbo --no-ignition" \
            #          --user-data-dir=/tmp/${NAME} --new-window --no-sandbox --disable-hang-monitor -incognito -enable-nacl &> /dev/null & #&>${TAG}logs/${NAME}_log_file &#& pkill chrome #> /dev/null &  #&>logs/${NAME}_log_file &

            if (( (idx-$start_line) % $max_num_window == 0 ))
            then
                    echo "Waiting to clean $idx and prev $max_num_window windows ... "
                    # timeout 30 out/Bytecode/chrome $url --js-flags="--taint_log_file=/media/data1/zfk/Documents/sanchecker/${TAG}crawl/$NAME --no-crankshaft --no-turbo --no-ignition" \
                    #  --user-data-dir=/tmp/${NAME} --new-window --no-sandbox --disable-hang-monitor -incognito -enable-nacl &>${TAG}logs/${NAME}_log_file && pkill chrome
                    sleep 30s
                    pkill chrome
                    sleep 2s
                    echo "$idx and prev $max_num_window windows cleaned! "
            #else

            fi
            #sleep ${sleep_time}s --user-data-dir=/tmp
    elif ((idx > $end_line))
    then
            echo "Come to the end $idx. Waiting to clean all windows ... "
            sleep 30s
            pkill chrome
            echo "All windows cleaned!"
            break
    fi
done < tranco_94Q2.csv

#TODO: delete useless lines