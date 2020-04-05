"""Regex to use as a Duplicati filter.
This may be added to in the future.
"""

import os
import sys
sys.path.append(os.path.normpath(__file__).rsplit(os.path.sep, 2)[0])
from regex_build import RegexBuild


with RegexBuild('.*') as build:
    # Exensions
    with build(r'\.') as extensions:
        extensions('(?i)', exit='$')(
            'temp', 'tmp', 'cache', 'dmp', 'dump', 'err', 'crash', 'part',
            RegexBuild('log')('', r'\..*'), RegexBuild('lock')('', 'file'),
        )
        extensions('reapeaks', 'pyc', 'updaterId', 'cprestoretmp')

    with build(r'\\') as paths:
        # Block specific files
        paths(
            'Thumbs.db', 'UsrClass.dat', 'output_log.txt',
            RegexBuild('hyberfil', 'swapfile')('.sys'),
            RegexBuild(r'LocalShaderCache-.*\.upk'),
        )

        # Block misc files
        paths('(?i)', exit='$')(
            'lock', 'temp', 'error', 'dump', 'dmp', 'cache', 'autoexec.bat',
            RegexBuild('log')('', r'\..*'), RegexBuild('lock')('', 'file'),
        )

        # Block specific folders
        paths(
            'Microsoft', 'NetHood', 'PrintHood', 'Recent', 'SendTo', 'LocalService', 'NetworkService', '__pycache__',
            'System Volume Information', 'RECYCLER', r'\$RECYCLE\.BIN', 'I386', 'MSOCache', 'Temporary Internet Files',
            r'Google\\Chrome\\Safe Browsing', 'site-packages', r'\.duplicacy', r'\.git', 'System Volume Information',
            'WUDownloadCache', 'OneDriveTemp', 'Config.MSI', 'Perflogs', RegexBuild('Windows')('', r'\.old'),
        )(r'\\')

        # Block misc folders
        with paths('(?i)', exit=r'\\$') as directories:
            directories(
                'temp', 'tmp', 'temporary', 'dmp', 'telemetry', 'local storage', '.backup', 'safebrowsing', 'installer',
                RegexBuild('', 'elevated')('diagnostics'), RegexBuild('hardware')('', ' ')('survey'),
                RegexBuild('crash')('', 'es', RegexBuild('', ' ', r'\-')('report', 'log', 'dump')('', 's')),
                RegexBuild(
                    RegexBuild('web')('', 'app'), 'shader', 'gpu', 'd2ds','code', 'cef', 'package',
                    'html', 'installer', 'data', 'file',
                )('', ' ', r'\-')('cache')('', r'\-temp'),
                RegexBuild('cache')('', 's', 'storage', RegexBuild('d')('', 'data', 'extensions', 'thumbnails')),
                RegexBuild('dump', 'minidump', 'error')('', 's'),
                RegexBuild('log')('', 's', 'files', 'backups'),
            )

        # Documents
        with paths(r'Documents\\') as documents:
            documents('3DMark*', r'3DS Max .*\\SimCache\\', r'Larian Studios\\.*\\LevelCache\\')(r'\\')

        # AppData
        with paths(r'AppData\\') as appdata:
            # Local
            with appdata(r'Local\\') as local:
                local('IconCache.db')
                local(
                    '\@nzxtcam-app-updater', 'Amazon Drive', 'ConnnectedDevicesPlatform', 'Downloaded Installations',
                    'Duplicati', 'GoToMeeting', 'Microsoft', r'MicrosoftEdge\\SharedCacheContainers', 'OneDrive',
                    'Packages', 'SquirrelTemp', 'CrashRpt', 'Comms', 'GitHubDesktop', '4kdownload.com',
                    RegexBuild('Package')('s', ' Cache'), RegexBuild('NVIDIA')('', ' Corporation'),
                    RegexBuild(r'acquisition\\')('sensitive_data', 'tabcache'), 'EpicGamesLauncher',
                    RegexBuild(r'UnrealEngine\\.*\\')('DerivedDataCache', 'Intermediate'),
                )(r'\\')

            # Roaming
            with appdata(r'Roaming\\') as roaming:
                roaming(r'NvTelemetryContainer\.log.*', r'ntuser\.dat', 'mntemp')
                roaming(
                    'NVIDIA', 'Amazon Cloud Drive', 'Code', 'CrashPlan', 'Jedi', r'Tencent\\TXSSO\\SSOTemp',
                    'uTorrent', 'vstelemetry', 'Github Desktop', 'FAHClient', 'Discord', 'Visual Studio Setup',
                    RegexBuild('NZXT')('', ' CAM'),
                    RegexBuild(r'Adobe\\.*')('CT Font ', 'FontFeature', 'Asset', 'Native')(r'Cache'),
                )(r'\\')

        # ProgramData
        paths(r'ProgramData\\')(
            'Microsoft.*', 'NVIDIA.*', 'NV_Cache', 'CrashPlan', 'Battle.net', 'Auslogics', 'Autodesk', 'GFACE',
            'Blizzard Entertainment', 'boost_interprocess', 'Duplicati', 'Epic', 'FLEXnet', r'Mozilla\\Updates',
            'Packages', 'Path of Building', 'Razer', r'Ubisoft\\Ubisoft Game Launcher', 'USO.*', 'Windows.*', '.mono',
            r'Adobe\\SLStore', 'AVAST Software', 'CloudBerryLab', 'EA .*', 'For Honor.*', 'Intel', 'Kaspersky Lab',
            'LiquidTechnologies', 'Oracle', 'Origin', r'regid\.[0-9]{4}\-[0-9]{2}.com.*', 'RuPlatform', 'Samsung',


        )(r'\\')

        # LocalLow
        paths(r'LocalLow\\')('Mozilla', r'.*\\Unity', r'Nolla_Games_Noita\\Save00\\world\\')

        # Mozilla Firefox
        # C:\Users\Peter\AppData\Roaming\Mozilla\Firefox\Profiles\xxxxxxxx.Default\datareporting\
        # C:\Users\Peter\AppData\Roaming\Mozilla\Firefox\Profiles\xxxxxxxx.Default\favicons.sqlite-wal
        # C:\Users\Peter\AppData\Roaming\Mozilla\Firefox\Profiles\xxxxxxxx.Default\startupCache\
        with paths(r'Firefox\\.*\\') as firefox:
            firefox('favicons', 'webappstore', 'cookies', 'content-prefs', 'formhistory')(r'\.sqlite.*')
            firefox(
                'storage', 'thumbnails', 'datareporting', 'cache2',
                RegexBuild('startup', 'jumpList')('Cache'),
            )(r'\\')

        # Google Chrome (it can be moved from AppData, so just check for "/Chrome/*")
        # C:\Users\Peter\AppData\Local\Google\Chrome\User Data\Default\ChromeDWriteFontCache
        # C:\Users\Peter\AppData\Local\Google\Chrome\User Data\Default\blob_storage\
        # C:\Users\Peter\AppData\Local\Google\Chrome\User Data\Default\JumpListIconsMostVisited\
        with paths(r'Chrome\\.*\\') as chrome:
            chrome('ChromeDWriteFontCache', 'Favicons.*', 'Google Profile.*', 'Cookies', 'Cookies-journal')
            chrome(
                'AutofillStrikeDatabase', 'blob_storage', 'BudgetDatabase', 'Service Worker',
                'data_reduction_proxy_leveldb', 'Download Service', 'Feature Engagement Tracker', 'File System',
                'GCM Store', 'IndexedDB', 'JumpListIcons.*', 'Platform Notifications', 'Search Logos',
                'shared_proto_db', 'Site Characteristics Database',' Storage', 'VideoDecodeStats',
                'Web Applications', 'Pepper.*'
            )(r'\\')

        # Steam games
        with paths(r'steamapps\\common\\') as steam:
            # Ignore official Skyrim packs
            # C:\Program Files (x86)\Steam\steamapps\common\Skyrim\Data\Skyrim - Meshes.bsa
            # C:\Program Files (x86)\Steam\steamapps\common\Skyrim\Data\Dragonborn.esm
            with steam(r'Skyrim\\Data\\', exit=RegexBuild(r'\.')('bsa', 'esm')) as skyrim:
                skyrim('Dawnguard', 'Dragonborn', 'HearthFires')
                with skyrim('Skyrim') as skyrim_data:
                    skyrim_data('')
                    with skyrim_data(' - ') as skyrim_packs:
                        skyrim_packs('Animations', 'Interface', 'Meshes', 'Misc', 'Sounds', 'Textures', 'Shaders')
                        skyrim_packs('Voices')('', 'Extra')


if __name__ == '__main__':
    print(build)
