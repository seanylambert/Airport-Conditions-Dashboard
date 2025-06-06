# FlightConditionsDashboard
<!-- Explain what the project is and how to run it -->
Local Development URL: http://127.0.0.1:8000/index.html

TERMINAL COMMANDS
Start HTTP web server:
```bash 
python -m http.server 8000
```

Run Flask App: 
```bash
python backend/app.py    
``` 

Recreate the Virtual Environment:
```bash
conda env create -f environment.yml
```

<!-- 
git remote add origin https://github.com/seanylambert/FlightConditionsDashboard.git
git branch -M main
git push -u origin main 
-->

<!--
## commit a branch
git add .
git commit -m "<Description>"
git push --set-upstream origin <currentBranchName>
-->

<!--
## pull the main branch
git checkout main          # switch to main branch
git pull origin main       # update it with the latest
-->

<!--
## create a new branch
git checkout -b <newBranchName>
-->

    [{  'metar_id': 770278864, 
        'icaoId': 'KRHV', 
        'receiptTime': '2025-06-05 19:50:21', 
        'obsTime': 1749152820, 
        'reportTime': '2025-06-05 20:00:00', 
        'temp': 25, 
        'dewp': 11, 
        'wdir': 180, 
        'wspd': 4, 
        'wgst': None, 
        'visib': '10+', 
        'altim': 1011.9, 
        'slp': None, 
        'qcField': 0, 
        'wxString': None, 
        'presTend': None, 
        'maxT': None, 
        'minT': None, 
        'maxT24': None, 
        'minT24': None, 
        'precip': None, 
        'pcp3hr': None, 
        'pcp6hr': None, 
        'pcp24hr': None, 
        'snow': None, 
        'vertVis': None, 
        'metarType': 'METAR', 
        'rawOb': 'KRHV 051947Z 18004KT 10SM SKC 25/11 A2988', 
        'mostRecent': 1, 
        'lat': 37.3331, 
        'lon': -121.82, 
        'elev': 37, 
        'prior': 5, 
        'name': 'San Jose/Reid-Hillview Arpt, CA, US', 
        'clouds': [{'cover': 'SKC', 'base': None}]}]



CSS NOTES
All the styling is handled by Tailwind’s compiler, which parses the class string and generates the appropriate CSS behind the scenes.
```bash
<div class="z-40 w-full transition-[top] ltr:left-0 rtl:right-0 group-[.non-sticky-nav]:top-[-72px] group-[.non-sticky-nav]:fixed group-[.non-sticky-nav]:xl:px-8 group-[.sticky-nav]:!top-0 duration-[400ms] ease-out"> 

z-40                             --> z-index: 40;
w-full                           --> width: 100%;
transition-[top]                 --> transition-property: top;
duration-[400ms]                 --> transition-duration: 400ms;
ease-out                         --> transition-timing-function: ease-out;
ltr:left-0                       --> left: 0 in LTR direction;
rtl:right-0                      --> right: 0 in RTL direction;
group-[.non-sticky-nav]:top-[-72px]  --> top: -72px when parent has class `.non-sticky-nav`;
group-[.non-sticky-nav]:fixed        --> position: fixed when parent has class `.non-sticky-nav`;
group-[.non-sticky-nav]:xl:px-8      --> padding-left/right: 2rem on `xl` screens if parent has `.non-sticky-nav`;
group-[.sticky-nav]:!top-0           --> override top to 0 if parent has `.sticky-nav`;
```

<!--  taken from https://nordvpn.com/creator/pricing/#compare-plans-desktop
<div class="z-40 w-full transition-[top] ltr:left-0 rtl:right-0 group-[.non-sticky-nav]:top-[-72px] group-[.non-sticky-nav]:fixed group-[.non-sticky-nav]:xl:px-8 group-[.sticky-nav]:!top-0 duration-[400ms] ease-out"> 
    <header class="group-[.sticky-nav]:bg-secondary group-[.non-sticky-nav]:max-w-[1600px] group-[.non-sticky-nav]:xl:rounded-full group-[.is-light]:xl:shadow-md group-[.sticky-nav]:xl:mt-3 ease-out mx-auto transition-colors bg-secondary"> 
        <a data-ga-slug="Skip to main content" class="align-bottom transition-colors ease-out focus-visible:outline-none focus-visible:shadow-focus text-accent hover:text-accent-hover active:text-accent-active group-[.sticky-nav]:mt-1 absolute font-medium top-1/2 translate-y-[-50%] ltr:left-[10%] rtl:right-[10%] p-3 focus-visible:bg-neutral-100 z-50 pointer-events-none focus-visible:pointer-events-auto text-transparent focus-visible:text-neutral-900" href="#header-end" tabindex="0" aria-labelledby="Skip to main content"> 
            <p class="">Link to Something</p> 
        </a> 
        <section data-section="Header" data-has-heading="false" class="group/section" data-index="0" id="Header_00"> 
            <div class="mx-auto max-w-[1600px] px-4 md:px-6 group-[.non-sticky-nav]:xl:px-8 group-[.sticky-nav]:ltr:xl:pl-6 group-[.sticky-nav]:ltr:xl:pr-4 group-[.sticky-nav]:rtl:xl:pr-6 group-[.sticky-nav]:rtl:xl:pl-4 group-[.sticky-nav]:sm:px-6 group-[.sticky-nav]:px-4 py-5 sm:py-4"> 
                <div class="compensate-height hidden pt-16"></div>   
                <nav class="flex items-center justify-between" aria-label="Main Menu" aria-labelledby="Main Navigation"> 
                <div class="header-nav border-primary"> 
                    <a data-ga-slug="Home" class="align-bottom transition-colors ease-out focus-visible:outline-none focus-visible:shadow-focus text-accent hover:text-accent-hover active:text-accent-active block" href="/" id="header-hp-link">   
                        <div class="min-w-[143px]"> 
                            <svg width="143" height="32" viewBox="0 0 143 32" fill="none" class="w-auto group-[.is-light]:group-[.desktop-header]:w-[124px] h-[24px] sm:h-auto" xmlns="http://www.w3.org/2000/svg"></svg> 
                        </div> 
                        <span class="sr-only">Link to Something Better</span>   
                    </a> 
                </div>  
                <div class="header-nav flex w-max items-center group-[.desktop-header]:!static group-[.mobile-header]:!static absolute bottom-[9999px]"></div> 
                </nav>
            </div>
        </section>  
    </header> 
    <hr class="border-solid border-t-md border-neutral-200 group-[.non-sticky-nav]:xl:hidden"> 
    <div id="header-end"></div> 
</div> 
-->
