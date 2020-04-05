"""Regex to use as a Duplicati filter.
This may be added to in the future.
"""

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
            'Thumbs.db', 'mntemp', 'UsrClass.dat', 'output_log.txt',
            RegexBuild('hyberfil', 'swapfile')('.sys'),
            RegexBuild('(?i)', exit='$')(r'ntuser\.dat.*'),
            RegexBuild(r'LocalShaderCache-.*\.upk'),
        )

        # Block files with no extension
        paths('(?i)', exit='$')(
            'lock', 'temp', 'error', 'dump', 'dmp', 'cache',
            RegexBuild('log')('', r'\..*'), RegexBuild('lock')('', 'file'),
        )

        # Block specific folders
        paths(
            'Windows', 'Microsoft', 'NetHood', 'PrintHood', 'Recent', 'SendTo', 'LocalService', 'NetworkService',
            'System Volume Information', 'RECYCLER', r'\$RECYCLE\.BIN', 'I386', 'MSOCache', 'Temporary Internet Files',
            r'Google\\Chrome\\Safe Browsing', 'site-packages', r'\.duplicacy', r'\.git', 'System Volume Information',
            'WUDownloadCache', '__pycache__',
        )(r'\\')

        # Block misc folders
        with paths('(?i)', exit=r'\\$') as directories:
            directories(
                'temp', 'tmp', 'temporary', 'dmp', 'telemetry', 'local storage', '.backup', 'safebrowsing',
                RegexBuild('', 'elevated')('diagnostics'), RegexBuild('hardware')('', ' ')('survey'),
                RegexBuild('crash')('', 'es', RegexBuild('', ' ', r'\-')('report', 'log', 'dump')('', 's')),
                RegexBuild(
                    RegexBuild('web')('', 'app'), 'shader', 'gpu', 'd2ds','code', 'cef', 'package', 'html', 'installer',
                )('', ' ', r'\-')('cache')('', r'\-temp'),
                RegexBuild('cache')('', '2', 's', 'storage', RegexBuild('d')('', 'data', 'extensions', 'thumbnails')),
                RegexBuild('dump', 'minidump', 'error')('', 's'),
                RegexBuild('log')('', 's', 'files'),
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
            appdata(r'Roaming\\')(
                'NVIDIA', 'Amazon Cloud Drive', 'Code', 'CrashPlan', 'Jedi', r'Tencent\\TXSSO\\SSOTemp',
                'uTorrent', 'vstelemetry', 'Github Desktop', 'FAHClient', 'Discord', 'Visual Studio Setup',
                RegexBuild('NZXT')('', ' CAM'),
                RegexBuild(r'Adobe\\.*')('CT Font ', 'FontFeature', 'Asset', 'Native')(r'Cache'),
            )(r'\\')

        # ProgramData
        # TODO: This needs improvement
        paths(r'ProgramData\\')('Microsoft.*', 'NVIDIA*', 'NV_Cache')(r'\\')

        # LocalLow
        paths(r'LocalLow\\')('Mozilla', r'.*\\Unity', r'Nolla_Games_Noita\\Save00\\world\\')

        # Mozilla Firefox
        # TODO: This needs improvement
        # C:\Users\Peter\AppData\Roaming\Mozilla\Firefox\Profiles\xxxxxxxx.Default\datareporting\
        # C:\Users\Peter\AppData\Roaming\Mozilla\Firefox\Profiles\xxxxxxxx.Default\favicons.sqlite-wal
        # C:\Users\Peter\AppData\Roaming\Mozilla\Firefox\Profiles\xxxxxxxx.Default\startupCache\
        with paths(r'Firefox\\.*\\') as firefox:
            firefox('favicons', 'webappstore')('.sqlite.*')
            firefox('storage', 'thumbnails', 'datareporting')(r'\\')
            firefox('startup', 'jumpList')(r'Cache\\')

        # Google Chrome (it can be moved from AppData, so just check for "/Chrome/*")
        # TODO: This needs improvement
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
    # .*(\.((?i)(temp|tmp|cache|dmp|dump|err|crash|part|log(|\..*)|lock(|file))$|(reapeaks|pyc|updaterId|cprestoretmp))|\\((Thumbs.db|mntemp|UsrClass.dat|output_log.txt|(hyberfil|swapfile).sys|(?i)ntuser\.dat.*$|LocalShaderCache-.*\.upk)|(?i)(lock|temp|error|dump|dmp|cache|log(|\..*)|lock(|file))$|(Windows|Microsoft|NetHood|PrintHood|Recent|SendTo|LocalService|NetworkService|System Volume Information|RECYCLER|\$RECYCLE\.BIN|I386|MSOCache|Temporary Internet Files|Google\\Chrome\\Safe Browsing|site-packages|\.duplicacy|\.git|System Volume Information|WUDownloadCache|__pycache__)\\|(?i)(temp|tmp|temporary|dmp|telemetry|local storage|.backup|safebrowsing|(|elevated)diagnostics|hardware(| )survey|crash(|es|(| |\-)(report|log|dump)(|s))|(web(|app)|shader|gpu|d2ds|code|cef|package|html|installer)(| |\-)cache(|\-temp)|cache(|2|s|storage|d(|data|extensions|thumbnails))|(dump|minidump|error)(|s)|log(|s|files))\\$|Documents\\(3DMark*|3DS Max .*\\SimCache\\|Larian Studios\\.*\\LevelCache\\)\\|AppData\\(Local\\(IconCache.db|(\@nzxtcam-app-updater|Amazon Drive|ConnnectedDevicesPlatform|Downloaded Installations|Duplicati|GoToMeeting|Microsoft|MicrosoftEdge\\SharedCacheContainers|OneDrive|Packages|SquirrelTemp|CrashRpt|Comms|GitHubDesktop|4kdownload.com|Package(s| Cache)|NVIDIA(| Corporation)|acquisition\\(sensitive_data|tabcache)|EpicGamesLauncher|UnrealEngine\\.*\\(DerivedDataCache|Intermediate))\\)|Roaming\\(NVIDIA|Amazon Cloud Drive|Code|CrashPlan|Jedi|Tencent\\TXSSO\\SSOTemp|uTorrent|vstelemetry|Github Desktop|FAHClient|Discord|Visual Studio Setup|NZXT(| CAM)|Adobe\\.*(CT Font |FontFeature|Asset|Native)Cache)\\)|ProgramData\\(Microsoft.*|NVIDIA*|NV_Cache)\\|LocalLow\\(Mozilla|.*\\Unity|Nolla_Games_Noita\\Save00\\world\\)|Firefox\\.*\\((favicons|webappstore).sqlite.*|(storage|thumbnails|datareporting)\\|(startup|jumpList)Cache\\)|Chrome\\.*\\((ChromeDWriteFontCache|Favicons.*|Google Profile.*|Cookies|Cookies-journal)|(AutofillStrikeDatabase|blob_storage|BudgetDatabase|Service Worker|data_reduction_proxy_leveldb|Download Service|Feature Engagement Tracker|File System|GCM Store|IndexedDB|JumpListIcons.*|Platform Notifications|Search Logos|shared_proto_db|Site Characteristics Database| Storage|VideoDecodeStats|Web Applications|Pepper.*)\\)|steamapps\\common\\Skyrim\\Data\\((Dawnguard|Dragonborn|HearthFires)|Skyrim(| - ((Animations|Interface|Meshes|Misc|Sounds|Textures|Shaders)|Voices(|Extra))))\.(bsa|esm)))
