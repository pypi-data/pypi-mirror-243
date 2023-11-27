import os, sys, json, time, datetime, requests
from dateutil.tz import tzutc
import __main__


def __setServer__(local):
    credDir = os.path.expanduser('~') + os.sep + '.skolo' + os.sep
    if local:
        credFile = credDir + 'skolo.local.credentials'
        server = 'http://localhost:5000'
    else:
        credFile = credDir + 'skolo.credentials'
        try:
            server = open(os.path.expanduser('~') + os.sep + '.skolo' + os.sep + 'config').readlines()[0].split('server=')[-1]
        except:
            server = 'https://skolocfd.com'
    return server, credFile


def __respOK__(response):
    return 'HTTPStatusCode' in response and response['HTTPStatusCode'] == 200 and not response['errors']


class conn():
    def __init__(self, useLocal=None):
        self.__reqSession__ = requests.Session()
        
        self.__server__, credFile = __setServer__(useLocal)
        
        if not os.path.exists(credFile):
            self._exc(401, 'Missing credentials. For information on generating valid credentials visit the link provided.', link=self.__server__ + '/docs?topic=Api#Configuring%20Credentials')
            self.__cred__ = 'None'
        else:
            self.__cred__ = open(credFile, 'r').readlines()[0]
        self._checkVersion()
        
        
    def _clearLine(self, text):
        if hasattr(self, 'verbose') and self.verbose:
            if hasattr(self, 'lastPrintLine') and self.lastPrintLine == text:
                return
            print(text)
            self.lastPrintLine = text
            return
        sys.stdout.write("\033[K") #clear line 
        print(text.replace('\n',''), end='\r', flush=True)
        
    
    def _checkVersion(self, force=False):
        # Check for package updates
        verFile = os.path.expanduser('~') + os.sep + '.skolo' + os.sep + 'skolo.versionCheck'
        import skolo
        if not os.path.exists(verFile) or force or datetime.datetime.fromtimestamp(os.path.getmtime(verFile)) + datetime.timedelta(days=7) < datetime.datetime.now():
            try:
                vMax = max(requests.get('https://pypi.org/pypi/skolo/json').json()['releases'].keys())
            except:
                vMax = skolo.__version__
            if skolo.__version__ != vMax:
                print('\nALERT: skolo-' + skolo.__version__ + ' is installed, but skolo-' + vMax + ' is available:\n    python -m pip install --upgrade skolo\n')
            with open(verFile, 'w') as f:
                pass
        
    
    def _genResp(self, HTTPStatusCode=200, errors=[], warnings=[], messages=[], link=''):
        return {k:v for k,v in locals().items() if k != 'self'}
        
        
    def _exc(self, code, errMsg, link='' ):
        if type(errMsg) ==  str:
            errMsg = [errMsg]
        
        errResp = self._genResp(code, errors=errMsg, link=link)
        if hasattr(__main__, '__file__') and ('cliparser' in __main__.__file__.lower() or os.path.basename(__main__.__file__) == 'skolo'):
            print(json.dumps(errResp, indent=4, sort_keys=True))
            sys.exit(-1)
        else:
            print('    ERROR ' + str(code) + ': ' + ' '.join(errMsg))
            print('      ' + link)
            return errResp
            #raise Exception(errMsg)
        
    
    def _buildResp(self, r):
        resp = {}
        if r.status_code == 401:
            resp = self._exc(r.status_code, 'Invalid credentials. For information on generating valid credentials visit the link provided.', link=self.__server__ + '/docs?topic=Api#Configuring%20Credentials')
        elif r.status_code == 403:
            resp = self._exc(r.status_code, 'Expired credentials. Please generate a new authentication token at the link provided.', link=self.__server__ + '/docs?topic=Api#Configuring%20Credentials')
        elif r.status_code == 404:
            resp = self._exc(r.status_code, r.text)
        elif r.status_code > 399:
            resp = self._exc(r.status_code, 'Unhandled server error - Please contact us.')
            
        if '[' not in r.text and '{' not in r.text:
            resp.update({'messages':[r.text]})
        else:
            resp = json.loads(r.text)
        resp.update({'HTTPStatusCode':r.status_code})
        return resp, r
        
        
    def _http(self, url, req, json=None, data=None, files=None):
        args = {'url':url, 'json':json, 'data':data, 'files':files, 'auth':(self.__cred__, 'none')}
        args = {k:v for k,v in args.items() if v != None}
        if 'files' not in args:
            args['headers'] = {'Content-Type': 'application/json'}
            
        try:
            return self._buildResp(getattr(self.__reqSession__, req)(**args))
        except requests.exceptions.ConnectionError:
            try:
                a = self.__reqSession__.get('http://www.google.com')
            except requests.exceptions.ConnectionError:
                resp = self._exc(500, 'Connection refused. It appears your internet connection is down.')
            resp = self._exc(500, 'Connection refused. It appears the Skolo server is unreachable.')
            return resp, None
    
    
    def _get(self, url, json={}):
        return self._http(url, 'get', json)
    
    
    def _post(self, url, json={}):
        return self._http(url, 'post', json)
    
    
    def _uploadFile(self, url, file, data):
        fd = {'file': ''}
        with open(file, 'rb') as fd['file']:
            return self._http(url, 'post', None, data, fd)
    
    
    def _buildUrl(self, pre, suf='', filters=True):
        if not filters:
            return self.__server__ + pre    
        return self.__server__ + pre + self._filterUrl(self.__filters__) + suf
    
    
    def _filterUrl(self, filters, ignore=[]):
        self.__filters__ = filters
        t = ''
        for k,v in filters.items():
            if k in ignore:
                continue
            t += '?' + k + '=' + v
        return t
    
    
    def checkExist(self):
        """
        Checks if the Skolo instance (Run, Orientation, etc.) exists on the server

        Returns
        -------
        response : dict
            Skolo HTTP response dictionary, see https://www.skolocfd.com/docs?topic=Api
            If the HTTPStatusCode in the dict is 200, the Run/Orientaton/etc. exists
        """
        url = self._buildUrl('/api/exists')
        return self._get(url)[0]
    
    
    def _listChildren(self):
        url = self._buildUrl('/api/list')
        return self._get(url)[0]



# Generic account connection
class acct(conn):
    def __init__(self, args):
        kD = {'project':'proj', 'run':'case', 'orien':'rh'}
        self.__filters__={}
        for key in ['project', 'proj', 'run', 'case', 'orien', 'rh']:
            if key in kD:
                target = kD[key]
            else:
                target = key
            if hasattr(args, key) and getattr(args, key):
                self.__filters__[target] = getattr(args, key)
        super(acct, self).__init__(args.local)
        self.checkExist()



class Run(conn):
    def __init__(self, proj, run, useLocal=False):
        """
        Initialize a connection to a Skolo Run

        Inputs
        ----------
        proj : string
            Skolo project name
        run : string
            Skolo run number
        useLocal : bool
            connect to local rather than remote server

        Returns
        -------
        run : object
            An instance of this class
        """
        
        self.proj = proj
        self.run = run
        self.__filters__ = {'proj':proj, 'case':run}
        super(Run, self).__init__(useLocal)
        self.checkExist()
        
        
    def listOrientations(self):    
        """
        Returns a list of all orientations for a given run; no inputs.
        """
        resp = self._listChildren()
        return resp['orienList']
    
    
    def createNew(self, comment, tag='None', copyGeometry=True, copyOrientations=True, copySettings=True, copyPostPro=True):
        """
        Function that creates a new run, based on the current run.

        Inputs
        ----------
        comment : string
            descriptive comment for the run
        tag : string
            descriptine tag for the run - equivalent to "topic" in the Skolo GUI
        copyGeometry : bool
            copy all geometry from the baseline run
        copyOrientations : bool
            copy all orientations from the baseline run
        copySettings : bool
            copy all run settings from the baseline run
        copyPostPro : bool
            copy all postPro templates from the baseline run

        Returns
        -------
        resp : dict
            Skolo HTTP response dictionary, see https://www.skolocfd.com/docs?topic=Api
        """
        
        jsonData = {'tag':tag, 'comment':comment, 'geometry':copyGeometry, 'settings':copySettings, 'orientations':copyOrientations, 'postpro':copyPostPro}
        url = self._buildUrl('/api/newCase')
        resp, r = self._post(url, jsonData)
                
        if r.status_code < 400:
            resp.update({'link':self.__server__ + '/case?proj=' + self.proj + '?case=' + resp['newRunName'] + '?step=settings'})
        
        return resp

        
        
# Connection to specific proj:run:orientation
class Orientation(conn):
    def __init__(self, proj, run, orien, useLocal=False):
        """
        Initialize a connection to a Skolo Orientation within a Run

        Inputs
        ----------
        proj : string
            Skolo project name
        run : string
            Skolo run number
        orien : string
            Skolo orientation
        useLocal : bool
            connect to local rather than remote server

        Returns
        -------
        run : object
            An instance of this class
        """
        self.proj = proj
        self.run = run
        self.orien = orien
        self.useLocal = useLocal
        self.__filters__ = {'proj':proj, 'case':run, 'rh':orien}
        super(Orientation, self).__init__(useLocal)
        self.checkExist()
    
    
    def _taskWatch(self, resp, cmd, queue, mins):
        watchUrl = self._buildUrl('/getStatus/' + resp['jobID'] + '/' + queue + '?fromApi=true', filters=False   )
        t, dt, tMax, status = 0, 1, 60*mins, 'queueing'
        while t < tMax and status not in ['finished', 'failed']:
            watch, w = self._get(watchUrl)
            status = watch['task']['status']
            
            if 'log' in watch['task']['meta'] and len(watch['task']['meta']['log']) > 0:
                lines = [line for line in watch['task']['meta']['log'] if not line.startswith(' ')]
                if lines != []:
                    self._clearLine(lines[-1])
            elif status != 'queueing':
                self._clearLine(cmd + ' job is ' + status)
            
            if 'geomCheckRhs' in watch['task']['meta']:
                watch['geomCheckRhs'] = watch['task']['meta']['geomCheckRhs']
            
            time.sleep(dt)
            t += dt
        print()
        watch['taskLog'] = watch['task']['meta']['log']
        watch['link'] = self._buildUrl('/case?proj=', '?step=upload')
        del(watch['task'])
        
        return watch
    
    
    def geomCompare(self):
        """
        Submits a geometry comparison job vs. the baseline

        Returns
        -------
        resp : dict
            Skolo HTTP response dictionary, see https://www.skolocfd.com/docs?topic=Api
        """

        cmd = 'geomCompare'
        suf = '?fromApi=true?fullCheck=false?debug=false'
        
        url = self._buildUrl('/compareGeom', suf)
        jsonData = {}
        resp, r = self._post(url, jsonData)
        
        # Catch case where server chooses not to run geomPrep
        if 'jobID' not in resp and 'rhError' in resp:
            resp['errors'] = [resp['rhError']]
            del resp['rhError']
            resp['HTTPStatusCode'] = 400
            return resp
        print(cmd.capitalize() + ' job is queueing', end='\r')
        
        # Watch job status
        return self._taskWatch(resp, cmd, 'geomQ', 5)
    
    
    def kinematics(self, force=False):
        """
        Submits kinematic model movement, and checks the resulting output geometry

        Inputs
        ----------
        force : bool
            forces re-running of kinematics for all rideheights whether needed or not - WARNING! overwrites files!

        Returns
        -------
        resp : dict
            Skolo HTTP response dictionary, see https://www.skolocfd.com/docs?topic=Api
        """
        
        resp = self._geomTask('kinematics', force=force)
        
        # geomCheck all the output rhs
        print("THIS IS THE RESP", resp)
        print(resp['geomCheckRhs'])
        for rh in resp['geomCheckRhs']:
            print("RIDEHEIGHT", rh)
            orien = Orientation(self.proj, self.run, rh, self.useLocal)
            orien.submit('setup')
        
        return resp
    
    
    def geomPrep(self, force=False):
        """
        Submits geomPrep, and checks the resulting output geometry

        Inputs
        ----------
        force : bool
            forces re-running of all geomPrep on all CAD files - WARNING! overwrites files!

        Returns
        -------
        resp : dict
            Skolo HTTP response dictionary, see https://www.skolocfd.com/docs?topic=Api
        """
        
        resp = self._geomTask('geomPrep', force=force)
        
        # geomCheck the output files
        self.submit('setup')
        
        return resp
    
    
    def _geomTask(self, cmd, force=False):
        """
        Submits geomPrep/kinematics
        
        Optional arguments:
            force:      forces re-running of all geomPrep on all CAD files - WARNING! overwrites files!
        """
        if self.orien != 'geomConstruction':
            return self._genResp(errors=['GeomPrep and Kinematics may only be run from the construion geometry orientation (geomConstruction)'])
        
        # Submit job
        suf = '?fromApi=true?rhSel=geomConstruction?fcnToRun=' + cmd
        if force:
            suf += '?forceReRun=true'
        
        
        url = self._buildUrl('/runGeomPrep', suf)
        
        print("URL", url)
        
        jsonData = {'files':[]}
        resp, r = self._post(url, jsonData)
        
        # Catch case where server chooses not to run geomPrep
        if 'jobID' not in resp and 'rhError' in resp:
            resp['errors'] = [resp['rhError']]
            del resp['rhError']
            resp['HTTPStatusCode'] = 400
            return resp
        print(cmd.capitalize() + ' job is queueing', end='\r')
        
        # Watch job status
        return self._taskWatch(resp, cmd, 'ansaQ', 20)
    
    
    def submit(self, cmd, costLimit=None):
        """
        Submits the current orientation with the desired command

        Inputs
        ----------
        cmd : string
            the command to run, which can be: setup, mesh, post, or submit (submit includes mesh, solve, post)
        costLimit : integer
            Specify a limit to acceptable estimated cost, above which job submission will be aborted

        Returns
        -------
        resp : dict
            Skolo HTTP response dictionary, see https://www.skolocfd.com/docs?topic=Api
        """
        
        if self.orien == 'geomCommon':
            return self._genResp(errors=['geomCommon is not a valid orientation. Such an orientation may only used by the upload command'])
        
        if cmd == None:
            cmd = 'submit'
        
        # Submit job
        suf = '?fromApi=true'
        if costLimit:
            float(costLimit)
            suf += '?costLimit=' + str(int(costLimit))
        
        url = self._buildUrl('/runBerd', suf)
        jsonData = {'cmd':cmd, 'rhSel':self.__filters__['rh']}
        resp, r = self._post(url, jsonData)
        print(cmd.capitalize() + ' job is queueing', end='\r')
        
        # Watch job status
        return self._taskWatch(resp, cmd, 'berdQ', 3)
        
        
    def _describeFile(self, f):
        return {'upload':True, 'size':os.path.getsize(f), 'mtime':str(datetime.datetime.fromtimestamp(os.path.getmtime(f), tz=tzutc()))}
        
        
    def upload(self, folder, force=False):
        """
        Uploads geometry to the orientation

        Inputs
        ----------
        folder : string
            the file or folder to upload.
            file - the file will always be uploaded
            folder - step, STL or CATIA files in the folder which are NOT already up-to-date on the server will be uploaded (speeds things up)
        force : bool
            force the upload of all files in the folder, even if they are already up-to-date on the server

        Returns
        -------
        resp : dict
            Skolo HTTP response dictionary, see https://www.skolocfd.com/docs?topic=Api
        """
        
        t0 = time.time()
        from concurrent.futures import ThreadPoolExecutor
        exts = ('.stl', '.stl.gz', '.vtp', '.vtp.gz', '.stp', '.step', 'catpart', '3dxml')
        
        # Create list of files
        files, tSize, t0 = {}, 0, time.time()
        if os.path.isdir(folder):
            for item in sorted(os.listdir(folder), key=str.casefold):
                if item.endswith(exts):
                    ful = folder + os.sep + item
                    files[ful] = self._describeFile(ful)
        elif os.path.exists(folder):
            files[folder] = self._describeFile(folder)
            force = True
        else:
            self._exc('Specified file location is neither a file nor a folder: ' + folder)
        
        # See which files are actually out-of-date on server
        if not force:
            url = self._buildUrl('/api/needsUpload')
            respNeed, r = self._get(url, json=files)
            for f in files:
                if f in respNeed['fileInfo'] and not respNeed['fileInfo'][f]['upload']:
                    files[f]['upload'] = False
        
        # Parallel uploading
        resp = {'HTTPStatusCode':200}
        url = self._buildUrl('/upload', '?units=Meters')
        def parUpload(geom):
            resp, r = self._uploadFile(url, geom, files[geom])
            self._clearLine('    Uploading: ' + geom)
            return (geom, resp)

        pool = ThreadPoolExecutor(max_workers=6)
        filesToUpload = sorted([item for item in files if force or respNeed['fileInfo'][item]['upload']], key=str.casefold)
        for geom in pool.map(parUpload, filesToUpload):
            if geom[1]['HTTPStatusCode'] == 200:
                files[geom[0]] = 'Upload successful'
                tSize += os.path.getsize(geom[0])
        self._clearLine('')
        
        if len(files) == 0:
            warnings = ['Zero suitable files (' + ', '.join(exts) + ') found at destination: ' + os.path.abspath(folder)]
        else:
            warnings = []

        resp = {'HTTPStatusCode':resp['HTTPStatusCode'], 'messages':['Uploaded %.1f Mb from %i files in %.1f sec.' % (tSize/(1024*1024), len(filesToUpload), time.time()-t0)], 'errors':[], 'warnings':warnings, 'fileInfo':files}
        resp['link'] = self._buildUrl('/case?proj=', '?step=upload')
        return resp