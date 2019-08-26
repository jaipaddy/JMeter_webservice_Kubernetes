#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#author - Jaishankar Padmanabhan
import os, subprocess, shlex, socket, logging, tarfile
from subprocess import PIPE, Popen
from flask import Flask, request, jsonify, stream_with_context, Response
from datetime import datetime
from google.cloud import storage

logging.basicConfig(format='[%(filename)s:%(lineno)s] %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

BUCKET_NAME=os.environ.get('BUCKET_NAME', None) 

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', None) 
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    logger.info('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))

def create_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
    logger.info('Created tarfile '+ os.path.basename(source_dir))    


app = Flask(__name__)
@app.route('/performancetest', methods=['GET', 'POST'])
def runtest():
    # Parse URL args
    script  = request.args.get('script', None)
    report  = request.args.get('report', None)
    workers = request.args.get('workers', None)
    testparam = request.args.get('testparam', None)
    testdir = '/jmeter/apache-jmeter-4.0/test/'
    
    if (script != None and report != None and workers != None and testparam != None):
        logger.info({'script': script, 'report': report, 'workers': workers, 'testparam': testparam})
    else:
        return jsonify({"Usage": "GET http://"+socket.getfqdn()+":5000/performancetest?script=sample.jmx&report=testreport&testparam=-Gthreads=34 -Gramp=5 -Grps=4&workers=192.168.128.1,192.168.128.2"})
    
    # Pass args to bash to run the test
    now = datetime.now()
    time = now.strftime("%Y-%m-%d_%H-%M-%S")
    
    command = shlex.split("jmeter -n -l performanceresults/results_" + time +".csv -t "+testdir+script + " -e -o performanceresults/"+report+"_"+time+ " "+testparam+" -R "+workers)
  
    def generate():
        yield '*** Thank you for using PEAS! Your performance test - '+script+' is now running ***'
        process = subprocess.Popen(command, stdout=PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        for line in iter(process.stdout.readline,''):
            yield '<pre>' +line.rstrip() + '<br> </pre>'
        # Compress and upload report dir
        if os.path.exists("performanceresults/"+report+"_"+time + "/index.html"):
                create_tarfile("performanceresults/"+report+"_"+time+ ".tar.gz", "performanceresults/"+report+"_"+time)
                upload_blob(BUCKET_NAME, "performanceresults/"+report+"_"+time+ ".tar.gz", report+"_"+time+ ".tar.gz")
                yield '\n\n *** Access your test report at https://storage.cloud.google.com/'+BUCKET_NAME+'/'+report+ '_'+ time+'.tar.gz?authuser=0 ***  '
        else:
            yield '*** The test did not produce a report because the test either failed or was aborted. Verify test parameters. ***'

    return Response(generate(), mimetype='text/html')



@app.route('/healthcheck', methods=['GET'])
def gethealth():
        return jsonify({"Usage": "GET http://"+socket.getfqdn()+":5000/performancetest?script=sample.jmx&report=testreport&testparam=-Gthreads=34 -Gramp=5 -Grps=4&workers=192.168.128.1,192.168.128.2"})
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
