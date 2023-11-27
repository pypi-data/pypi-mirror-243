#!/usr/bin/env python
import os, sys, json, argparse, webbrowser
import skolo
from skolo.caseObjects import acct, __setServer__, __respOK__


def checkCred(local):
    server, credFile = __setServer__(local)
    if not os.path.exists(credFile):
        print('\nMust exit: credentials not found:', credFile)
        print('    This tool requires access to the Skolo platform, via credentialed tokens provided under your username')
        print('    Please visit the link below for instructions on downloading and installing these credentials')
        print('\n    ' + server + '/docs?topic=Api#Configuring%20Credentials\n')
        sys.exit()


def printResponse(resp, args):
    print(json.dumps(resp, indent=4, sort_keys=True))
    if hasattr(args, 'browser') and args.browser and 'link' in resp:
        webbrowser.open(resp['link'])


def LIST(args):
    resp = acct(args).__listChildren__()
    printResponse(resp, args)


def upload(args):
    orien = skolo.Orientation(args.project, args.run, args.orientation, args.local)
    printResponse(orien.upload(args.folder, args.force), args)


def geom(args):
    orien = skolo.Orientation(args.project, args.run, args.orientation, args.local)
    calls = []
    
    # geomPrep requires a geomPrep and checkGeom call
    if args.command in ['geomPrep', 'all']:
        calls.append({'fcn':orien.geomPrep, 'args':(args.force,)})
    
    # kinematics requires a geomPrep and several checkGeom calls
    if args.command in ['kinematics', 'all']:
        calls.append({'fcn':orien.kinematics, 'args':(args.force,)})
    
    # GeomCompare is simple
    if args.command in ['geomCompare', 'all']:
        calls.append({'fcn':orien.geomCompare, 'args':(args.force,)})
    
    # Call each of the functions, exiting if at any point one of them fails
    moreCalls = []
    for call in calls:
        resp = call['fcn'](*call['args'])
        
        if resp['HTTPStatusCode'] != 200:
            print('Exiting due to server failure')
            return
        elif resp['errors']:
            print('Exiting due to errors')
            return
    
    return


def create(args):
    run = skolo.Run(args.project, args.baseline, args.local)
    inArgs = {k:v for k,v in vars(args).items() if k in ['comment', 'tag', 'noGeometry', 'noOrientations', 'noSettings', 'noPostpro']}
    
    kwargs = {}
    for key in inArgs:
        if key.startswith('no'):
            kwargs[key.replace('no', 'copy')] = not inArgs[key]
        else:
            kwargs[key] = inArgs[key]
    printResponse(run.createNew(**kwargs), args)


def submit(args):
    orien = skolo.Orientation(args.project, args.run, args.orientation, args.local)
    printResponse(orien.submit(args.execute, args.costLimit), args)


def version(args):
    import requests
    latest = max(requests.get('https://pypi.org/pypi/skolo/json').json()['releases'].keys())
    print('SkoloCFD CLI')
    print('  Current version:', skolo.__version__)
    print('  Latest version: ', latest)
    if latest != skolo.__version__:
        print('\n  You can upgrade with:\n    python -m pip install --upgrade skolo')


def main():
    # create the top-level parser
    parser = argparse.ArgumentParser(prog='skolo', description='skolo is the command line tool for the SkoloCFD cloud platform')
    parser.add_argument('-l', '--local', help='Connect to a Skolo server hosted locally', action='store_true')
    parser._positionals.title = 'Available commands'
    subparsers = parser.add_subparsers(help='--Command Description--')

    # create the parser for the "list" command
    parserList = subparsers.add_parser('list', help='LIST projects, runs, or orientations', description='LIST will display all exiting projects (default), runs (if given a project) or orientations (if given a run and project)')
    parserList.add_argument('-p', '--project', help='Specify a project to list all runs')
    parserList.add_argument('-r', '--run', help='Specify a run number to list orientations')
    parserList.set_defaults(func=LIST)
    parserList._positionals.title = 'Required arguments'

    # create the parser for the "create" command
    parserCreate = subparsers.add_parser('create', help='CREATE a new run', description='CREATE allows you to generate new runs referenced to a baseline.')
    parserCreate.add_argument('project', help='Specify the project')
    parserCreate.add_argument('baseline', help='Set the baseline run on which the new case is based')
    parserCreate.add_argument('comment', help='Description for the run')
    parserCreate.add_argument('-g', '--noGeometry', help='Do not copy geometry from the baseline run', action='store_true')
    parserCreate.add_argument('-t', '--tag', help='Tag for the run - useful for searching project tables')
    group = parserCreate.add_argument_group('optional overrides: by default, postPro templates, orientations, & settings from the baseline are copied to the new run. To override this one-by-one')
    group.add_argument('-no', '--noOrientations', help='Dont\' copy orientations from the baseline run.', action='store_true')
    group.add_argument('-np', '--noPostpro', help='Don\'t copy post-pro templates from the baseline run', action='store_true')
    group.add_argument('-ns', '--noSettings', help='Dont\' copy run settings from the baseline run.', action='store_true')
    parserCreate.add_argument('-b', '--browser', help='Open a browser tab for the new case upon completion.', action='store_true')
    parserCreate.set_defaults(func=create)
    parserCreate._positionals.title = 'Required arguments'

    # create the parser for the "upload" command
    parserUpload = subparsers.add_parser('upload', help='UPLOAD geometries to a run/orientation', description='UPLOAD allows you to upload a list or folder of files. All allowable filetypes (stl & stl.gz) will be uploaded. Other filetypes will be ignored.')
    parserUpload.add_argument('project', help='Specify the project')
    parserUpload.add_argument('run', help='Specify the run number')
    parserUpload.add_argument('orientation', help='Specify the orientation.\nSetting "geomCommon" as the orientation will upload to a directory shared by all current and future orientations.')
    parserUpload.add_argument('-f', '--folder', help='Folder or file to upload')
    parserUpload.add_argument('--force', help='By default, only files newer than any on the server are. This option forces a fresh upload.', action='store_true')
    parserUpload.add_argument('-b', '--browser', help='Open a browser tab for the new case upon completion.', action='store_true')
    parserUpload.set_defaults(func=upload)
    parserUpload._positionals.title = 'Required arguments'

    # create the parser for the "geom" command
    parserGeom = subparsers.add_parser('geom', help='Process GEOM for a run', description='GEOM allows you to process CAD, perform kinematics, compare to a baseline, or perform all 3 in sequence')
    parserGeom.add_argument('project', help='Specify the project')
    parserGeom.add_argument('run', help='Specify the run number')
    parserGeom.add_argument('orientation', help='Specify which orientation, most commonly geomConstruction')
    parserGeom.add_argument('command', help='Command to execute in a comma separated list.', choices=['geomPrep', 'kinematics', 'geomCompare', 'all'])
    parserGeom.add_argument('-b', '--browser', help='Open a browser tab to view results upon completion.', action='store_true')
    parserGeom.add_argument('-f', '--force', help='Forcibly re-run the command(s) specified. Warning: this may overwrite files!', action='store_true')
    parserGeom.set_defaults(func=geom)
    parserGeom._positionals.title = 'Required arguments'

    # create the parser for the "submit" command
    parserSubmit = subparsers.add_parser('submit', help='SUBMIT an orientation for solving', description='SUBMIT allows you to run the specified orientation.')
    parserSubmit.add_argument('project', help='Specify the project')
    parserSubmit.add_argument('run', help='Specify the run number')
    parserSubmit.add_argument('orientation', help='Specify which orientation')
    parserSubmit.add_argument('-e', '--execute', help='Command to execute. Default is "submit" Other options allow you to perform only setup, meshing, or post processing.', choices=['setup', 'mesh', 'submit', 'post'])
    parserSubmit.add_argument('-c', '--costLimit', help='Set a cost limit, above which the operation will not execute.', type=int)
    parserSubmit.add_argument('-b', '--browser', help='Open a browser tab for the new case upon completion.', action='store_true')
    parserSubmit.set_defaults(func=submit)
    parserSubmit._positionals.title = 'Required arguments'

    # create the parser for the "version" command
    parserSubmit = subparsers.add_parser('version', help='List current and latest version', description='VERSION lists the current and latest version')
    parserSubmit.set_defaults(func=version)
    parserSubmit._positionals.title = 'Required arguments'

    # Parse and run function
    args = parser.parse_args()
    
    # Check credentials are installed
    checkCred(args.local)
    
    # Run the chosen function
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()