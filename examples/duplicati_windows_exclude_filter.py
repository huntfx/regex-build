"""Regex to use as a Duplicati filter.
This may be added to in the future.

Using a one liner like this provided a massive speed increase compared
to using a lot of simple filters.
"""

import os
import subprocess
import sys

sys.path.append(os.path.normpath(__file__).rsplit(os.path.sep, 2)[0])
from regex_build import RegexBuild


test_filter = lambda filter, source='C:/': subprocess.Popen([
    'C:/Program Files/Duplicati 2/Duplicati.CommandLine.exe',
    'test-filter',
    source,
    '--exclude="[{}]"'.format(filter),
], stdout=sys.stdout)


with RegexBuild() as main:
    with main(r'C:\\') as c:
        c('NVIDIA')(r'\\')
        with c(r'Users\\.*\\') as userdir:
            userdir(r'\.gitconfig')
            userdir(
                'OneDrive', 'searches', 'Favorites', 'Links', 'MicrosoftEdgeBackups', 'Cookies', 'Local Settings', 'Templates',
                'Start Menu', 'Application Data', RegexBuild('My ')('Documents', 'Videos', 'Pictures', 'Music'),   # Inaccessible system folders
                'hpremote' # HP Remote Graphics Software logs
                r'Autodesk\\Genuine Service',
                #r'\.(?!vscode).+',  # Ignore all ".<name>" folders aside from Visual Studio Code
                r'\..*',  # Ignore all ".<name>" folders
                r'\.pyenv',  # Python installations
            )(r'\\')

    with main('.*') as build:
        # Block Exensions
        with build(r'\.', exit='$') as extensions:
            extensions('(?i)')(
                'temp', 'tmp', 'cache', 'dmp', 'dump', 'err', 'crash', 'part', 'localstorage',
                'vhdx', # Virtual file system disks
                RegexBuild('log')('', r'\..*'), 'lock[a-zA-Z0-9_-]*',
            )('(?-i)')
            extensions('reapeaks', 'pyc', 'updaterId', 'cprestoretmp')

        # Block specific files
        build(
            'Thumbs.db', 'UsrClass.dat', 'output_log.txt',
            RegexBuild('hyberfil', 'swapfile')('.sys'),
            RegexBuild(r'LocalShaderCache-.*\.upk'),
        )('$')

        build('(?i)')(
            # Block specific files that may be any case
            r'ntuser\.dat.*', 'autoexec.bat',

            # Block misc files that may not have extensions
            'temp', 'error', 'dump', 'dmp',
            RegexBuild('log')('', r'\..*'), RegexBuild('lock')('', 'file', '_.*'), RegexBuild('cache')('', r'\.json'),
        )('(?-i)$')

        # Block specific folders
        build(
            'Microsoft', 'NetHood', 'PrintHood', 'Recent', 'SendTo', 'LocalService', 'NetworkService', '__pycache__',
            'System Volume Information', 'RECYCLER', r'\$RECYCLE\.BIN', 'I386', 'MSOCache', 'Temporary Internet Files',
            r'Google\\Chrome\\Safe Browsing', r'\.duplicacy', r'\.git', 'System Volume Information',
            'WUDownloadCache', 'OneDriveTemp', 'Config.MSI', 'Perflogs', RegexBuild('Windows')('', r'\.old'),
            r'Epic Games\\Launcher\\VaultCache',
            'site-packages',  # Python
            '_gsdata_',  # GoodSync
            '.tmp.drivedownload',  # Google Backup & Sync
        )(r'\\')

        # Block misc folders
        build('(?i)')(
            'tmp', 'dmp', 'telemetry', 'local storage', r'\.backup', 'safebrowsing', 'installer',
            RegexBuild('temp')('', 'orary', 'data'),
            RegexBuild('', 'elevated')('diagnostics'), RegexBuild('hardware')('', ' ')('survey'),
            RegexBuild('crash')('', 'es', RegexBuild('', ' ', r'\-')('report', 'log', 'dump')('', 's')),
            RegexBuild(
                RegexBuild('web')('', 'app'), 'shader', 'gpu', 'd2ds','code', 'cef', 'package',
                'html', 'installer', 'data', 'file',
            )('', ' ', r'\-')('cache'),  # Lots of cache folder types
            RegexBuild('cache')('', 's', 'storage', RegexBuild('d')('', 'data', 'extensions', 'thumbnails')),
            RegexBuild('dump', 'minidump', 'error')('', 's'),
            RegexBuild('log')('', 's', 'files', 'backups'),
        )(r'(?-i)\\')

        # Documents
        with build(r'Documents\\') as documents:
            # Adobe folder
            with documents(r'Adobe\\') as adobe:
                with adobe(r'Adobe Media Encoder\\[0-9]*\.[0-9]*\\') as media_encoder:
                    media_encoder('Media Browser Provider Exception', RegexBuild('AMEEncoding')('', 'Error')(r'Log\.txt$')) # D:\Peter\Documents\Adobe\Adobe Media Encoder\11.0\AMEEncodingErrorLog.txt
                adobe(r'After Effects [A-Z0-9 ]*\\AE Project Logs\\') # D:\Peter\Documents\Adobe\After Effects CS6\AE Project Logs

            # Example Unreal Engine projects
            documents(r'Unreal Projects\\')(
                'ABoyandHisKite', 'AllegorithmicGynoid', 'Blueprints', 'ChaosDestructionDemo','ContentExamples',
                'CouchKnights', 'ElementalDemo', 'EpicZenGarden', 'InfiltratorDemo', 'MultiplayerShootout',
                'PixelStreamingDemo', 'PlatformerGame', 'PortalsBlueprint', 'RealisticRendering', 'Reflections',
                'ShooterGame', 'ShowdownVRDemo', 'SubstanceAtlantis', 'SciFiBunk', 'SillyGeo', 'VehicleGame',
            )(r'\\')

            with documents(r'My Games\\') as games:
                games(r'Titan Quest')('', ' - Immortal Throne')(r'\\SaveData\\Main\\_.*\\PlayerTmp0000\.chr')

                with games(r'Path of Exile\\') as poe:
                    poe(r'PoE-[0-9]*-[0-9]*-[0-9]*\.dmp')('', r'\.txt')('$')
                    poe('Minimap', 'OnlineFilters')(r'\\')

            # General folders
            documents(
                r'3DS Max [0-9]{4}\\SimCache',
                RegexBuild('3DMark')('', 'Farandole')(r'\\Shaders'),
                RegexBuild(r'Larian Studios\\Divinity Original Sin')('', ' Enhanced Edition')(r'\\LevelCache'),
            )(r'\\')

        # AppData
        with build(r'AppData\\') as appdata:
            # Local
            with appdata(r'Local\\') as local:
                # General files
                local(
                    r'IconCache\.db', r'SageThumbs\.db3',
                    r'LooksBuilder\\CurrentSession.ls3',
                    r'Resmon\.ResmonCfg'  # Resource monitor config
                    r'Saber\\WWZ\\client\\render\\pso_cache',  # World War Z cache
                    'ExpanDrive',  # ExpanDrive cache
                    r'Arma 3\\[a-z]{4}3_[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-2][0-9]-[0-6][0-9]-[0-6][0-9]\.rpt',  # \AppData\Local\Arma 3\arma3_2014-05-30_22-30-01.rpt
                )('$')
                # General folders
                local(
                    '\@nzxtcam-app-updater', 'nzxt cam-updater', 'Amazon Drive', 'ConnectedDevicesPlatform',
                    'Duplicati', 'GoToMeeting', 'Microsoft', r'MicrosoftEdge\\SharedCacheContainers', 'OneDrive',
                    'Packages', 'SquirrelTemp', 'CrashRpt', 'Comms', 'GitHub', 'GitHubDesktop', '4kdownload.com',
                    'Apps', r'Dropbox\\Update', 'FluxSoftware', r'id Software\\quakelive', 'IsolatedStorage',
                    'Last.fm', r'Mozilla\\updates', 'Native Instruments', 'Origin', 'PunkBuster', 'Razer',
                    'assembly', r'Skype\\Apps', 'Spotify', 'TeamViewer', r'THQ\\Saints Row 2\\ads', 'Warframe',
                    r'BBC\\BBC iPlayer Downloads', r'Battle\.net', 'GoodSync', 'Blizzard Entertainment', 'CEF',
                    'VirtualStore', 'chia-blockchain', 'Oculus', 'Everything', 'Mozilla', 'Discord',
                    'bitwarden-updater', 'UnrealEngine', 'Downloaded Installations', 'Overwolf',
                    'History', 'Application Data',  # Inaccessible system folders
                    'REDEngine',  # Cyberpunk cache
                    'Programs',  # Local installations
                    RegexBuild('Package')('s', ' Cache'), RegexBuild('NVIDIA')('', ' Corporation'),
                    RegexBuild('Ubisoft')('', ' Game Launcher'),
                    RegexBuild(r'acquisition\\')('sensitive_data', 'tabcache'), 'EpicGamesLauncher',
                    RegexBuild(r'UnrealEngine\\.*\\')('DerivedDataCache', 'Intermediate'),
                )(r'\\')
                # Exclude all Google/Mozilla directories aside from Chrome/Firefox
                local(r'Google\\(?!Chrome\\).+'),

            # Roaming
            with appdata(r'Roaming\\') as roaming:
                # Adobe stuff
                with roaming(r'Adobe\\') as adobe:
                    # C:\Users\Peter\AppData\Roaming\Adobe\Adobe Photoshop 2020\Adobe Photoshop 2020 Settings\web-cache-temp
                    adobe(
                        'CRLogs', 'GUDE', 'Flash Player', 'OOBE', 'Common',
                        RegexBuild(r'Adobe Photoshop [0-9]{4}\\')(
                            RegexBuild('CT Font ', 'FontFeature')('Cache'),
                            RegexBuild(r'Adobe Photoshop [0-9]{4} Settings\\web-cache-temp'),
                        )
                    )(r'\\')
                    adobe(r'Color\\ACEConfigCache2.lst')

                # Handbrake
                with roaming('HandBrake') as handbrake:
                    handbrake(r'hb_queue[0-9*]\.json')

                # General files
                roaming(r'NvTelemetryContainer\.log.*', 'mntemp')
                # General folders
                roaming(
                    'NVIDIA', 'Amazon Cloud Drive', 'Code', 'CrashPlan', r'Tencent\\TXSSO\\SSOTemp',
                    'uTorrent', 'vstelemetry', 'GitHub Desktop', 'FAHClient', 'Visual Studio Setup',
                    r'AirLiveDrive\\DisksCache', 'Guild Wars 2', 'Apple Computer', 'Autodesk', r'Battle\.net',
                    'InstallShield Installation Information', r'\.mono', 'Zoom', 'vlc', 'EasyAntiCheat',
                    r'Macromedia\\Flash Player', 'Chia Blockchain', 'Oculus', 'Spotify', r'Teracopy\\History',
                    'gcloud', 'Bitwarden', 'OculusClient', 'ente', 'Jedi',
                    RegexBuild('(?i)discord')('', 'sdk')('(?-i)'),
                    RegexBuild('NZXT')('', ' CAM'), 'CAM',
                    r'Fatshark\\Darktide\\EBWebView',
                )(r'\\')

            # Mozilla Firefox
            # C:\Users\Peter\AppData\Roaming\Mozilla\Firefox\Profiles\xxxxxxxx.Default\datareporting\
            # C:\Users\Peter\AppData\Roaming\Mozilla\Firefox\Profiles\xxxxxxxx.Default\favicons.sqlite-wal
            # C:\Users\Peter\AppData\Roaming\Mozilla\Firefox\Profiles\xxxxxxxx.Default\startupCache\
            with build(r'Mozilla\\Firefox\\Profiles\\') as firefox_profiles:
                with firefox_profiles(r'.*\\') as firefox_profile:
                    firefox_profile(
                        'crashes', 'shader-cache', 'datareporting', 'cache2',
                        RegexBuild('startup', 'jumpList')('Cache'),
                    )(r'\\')

            # LocalLow
            with appdata(r'LocalLow\\') as locallow:
                locallow(
                    'Apple Computer', 'Oracle', 'Mozilla', 'Sony Online Entertainment', 'Sun', 'Unity',
                    'Oculus',
                    r'Nolla_Games_Noita\\Save00\\world',  # Noita world
                    r'.*\\Unity',  # Unity games have a folder at 2nd level
                )(r'\\')

                # Only back up Google Earth places
                with build(r'Google\\', exit='.+') as google:
                    google(r'(?!GoogleEarth\\)')
                    with google(r'GoogleEarth\\') as earth:
                        earth(r'(?!myplaces\.kml$)')

        # ProgramData
        build(r'ProgramData\\')(
            'Microsoft.*', 'NVIDIA.*', 'NV_Cache', 'CrashPlan', 'Battle.net', 'Auslogics', 'Autodesk', 'GFACE',
            'Blizzard Entertainment', 'boost_interprocess', 'Duplicati', 'Epic', 'FLEXnet', r'Mozilla\\Updates',
            'Packages', 'Path of Building', 'Razer', r'Ubisoft\\Ubisoft Game Launcher', 'USO.*', 'Windows.*', r'\.mono',
            r'Adobe\\SLStore', 'AVAST Software', 'CloudBerryLab', 'EA .*', 'For Honor.*', 'Intel', 'Kaspersky Lab',
            'LiquidTechnologies', 'Oracle', 'Origin', r'regid\.[0-9]{4}\-[0-9]{2}.com.*', 'RuPlatform', 'Samsung',
        )(r'\\')

        # Google Chrome (it can be moved from AppData, so just check for "/Chrome/*")
        # C:\Users\Peter\AppData\Local\Google\Chrome\User Data\Default\ChromeDWriteFontCache
        # C:\Users\Peter\AppData\Local\Google\Chrome\User Data\Default\blob_storage\
        # C:\Users\Peter\AppData\Local\Google\Chrome\User Data\Default\JumpListIconsMostVisited\
        with build(r'Chrome\\.*\\') as chrome:
            chrome('ChromeDWriteFontCache', 'Favicons.*', 'Google Profile.*', 'Cookies', 'Cookies-journal')
            chrome(
                'AutofillStrikeDatabase', 'blob_storage', 'BudgetDatabase', 'Service Worker',
                'data_reduction_proxy_leveldb', 'Download Service', 'Feature Engagement Tracker', 'File System',
                'GCM Store', 'IndexedDB', 'JumpListIcons.*', 'Platform Notifications', 'Search Logos',
                'shared_proto_db', 'Site Characteristics Database',' Storage', 'VideoDecodeStats',
                'Web Applications', 'Pepper.*'
            )(r'\\')

        # Steam games
        with build(r'steamapps\\common\\') as steam:
            steam(r'.*\\steam_shader_cache\\')

            # Ignore official DS1 resources
            with steam(r'Dungeon Siege 1\\Resources\\') as dsres:
                dsres('Logic', 'Objects', 'Sound', 'Terrain', 'Voices')(r'\.dsres$')

            # Ignore official Skyrim packs
            # C:\Program Files (x86)\Steam\steamapps\common\Skyrim\Data\Skyrim - Meshes.bsa
            # C:\Program Files (x86)\Steam\steamapps\common\Skyrim\Data\Dragonborn.esm
            with steam(r'Skyrim\\') as skyrim:
                skyrim('TESV.exe')
                skyrim('DirectX10', 'DotNetFX', 'VCRedist')(r'\\')
                with skyrim(r'Data\\', exit=RegexBuild(r'\.')('bsa', 'esm')('$')) as data:
                    data('Dawnguard', 'Dragonborn', 'HearthFires')
                    with data('Skyrim') as data_file:
                        data_file('')
                        with data_file(' - ') as data_type:
                            data_type('Animations', 'Interface', 'Meshes', 'Misc', 'Sounds', 'Textures', 'Shaders')
                            data_type('Voices')('', 'Extra')

            # Ignore all standard Beat Saber files
            with steam(r'Beat Saber\\') as beat_saber:
                with beat_saber(r'Beat Saber_Data\\') as beat_saber_data:
                    beat_saber_data(r'[.\w-]+')('$')  # All files
                    beat_saber_data('Managed', 'Plugins', 'Resources', 'StreamingAssets', 'UnitySubsystems')(r'\\')  # Specific folders
                beat_saber('DLC', 'Libs')(r'\\')  # Specific folders
                beat_saber(r'Unity.*\.')('dll', 'exe')  # Specific files

        # Only allow Plex database (\Plex Media Server\Plug-in Support\Databases\com.plexapp.plugins.library.db)
        # This requires a bit of a hacky setup to force Duplicati to check inside the folders
        with build(r'Plex Media Server\\', exit='.+') as plex:
            plex(r'(?!Plug-in Support\\)')
            with plex(r'Plug-in Support\\') as plugins:
                plugins(r'(?!Databases\\)')
                with plugins(r'Databases\\') as databases:
                    databases(r'(?!com\.plexapp\.plugins\.library\.db$)')


if __name__ == '__main__':
    print(build)
