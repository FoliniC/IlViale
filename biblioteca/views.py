import threading
import re
import os
from django.http import HttpResponse
from django.core.cache import cache
from django.shortcuts import redirect  # Add this import at the top
import requests
#from bs4 import BeautifulSoup
import time
import random
import logging
import sys  
from datetime import timedelta, datetime
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

logger = logging.getLogger(__name__)

AFD_PROXY_URL = "https://provaltellina-bza5fpedf8ejehb5.z02.azurefd.net"  # Your AFD endpoint
AFD_HEADERS = {
    "X-Azure-FDID": "271ec543-e9df-490e-bda3-035bc78071a4",  # For request validation
    "X-Forwarded-For": "4.232.134.237"    # If backend needs original IP
}
# Configure session with retry strategy
session = requests.Session()
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504],
    allowed_methods=["GET"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
session.mount("http://", adapter)

def RobotsTxtView(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def async_refresh_content():
    """Background task with AFD routing"""
    logger = logging.getLogger('biblioteca')
    logger.warning("Starting background refresh with longer timeout")
    try:
        logger.warning("Setting up session for background refresh")
        CACHE_KEY = 'provaltellina_content_v4'
        CACHE_TIMESTAMP_KEY = 'provaltellina_last_fetch'
        # Route through AFD instead of direct call
        afd_target_url = f"{AFD_PROXY_URL}/projects/spazio-ellida-sala-multifunzionale-sostenibile-per-cultura-e-inclusione/"
        logger.warning(f"Background refresh URL: {afd_target_url}")
        session = requests.Session()
        logger.warning("Session created for background refresh")
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        logger.warning("Retry strategy configured for session")
        adapter = HTTPAdapter(max_retries=retry_strategy)
        logger.warning("Adapter created with retry strategy")
        session.mount("https://", adapter)
        logger.warning("Session mounted with HTTPS adapter")
        session.mount("http://", adapter)
        logger.warning("Session mounted with HTTP adapter")
        logger.warning("Session configured with retry strategy")



        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            # ... (keep your existing headers) ...
        }

        # Request goes through AFD proxy
        response = session.get(
            afd_target_url,
            headers=headers,
            timeout=15
        )
        logger.warning("Initial cookie request completed with longer timeout")
        time.sleep(random.uniform(1, 3))
        logger.warning(f"Main request completed with status {response.status_code}")
        response.raise_for_status()
        logger.warning("Response status is OK (200)")

        # # Process content
        # soup = BeautifulSoup(response.text, 'html.parser')
        # for script in soup.find_all('script'):
        #     if 'fingerprint' in str(script).lower():
        #         script.decompose()
        
        # title_tag = soup.find('h1')
        # if title_tag:
        #     title_tag.string = "3292 - spazio Ellida"
        
        content = response.text
        #content = content.replace("2.520", "4.200")
                # Add your modifications
        content = content.replace(
            "titolo del progetto e bando di riferimento", 
            "3292 - spazio Ellida"
        ).replace("2.520", "4.200")

        logger.warning("Content processed successfully")
        # Update cache
        cache.set(CACHE_KEY, content, 1800)
        cache.set(CACHE_TIMESTAMP_KEY, time.time(), 3600)
        logger.warning("Background refresh succeeded with longer timeout")
        
    except Exception as e:
        logger.error(f"Background refresh failed: {str(e)}")

def biblioteca_redirect(request):
    return redirect('https://mailchi.mp/e4fc2f1a5400/ellida')


def _inject_snapshot_banner(content, snapshot_path):
    try:
        created_dt = datetime.fromtimestamp(os.path.getmtime(snapshot_path)).strftime('%d/%m/%Y')
    except Exception:
        created_dt = 'sconosciuta'

    banner = f"""
    <div id="snapshot-banner" style="margin-top:30px; color:#666; font:11px/1.4 Arial,sans-serif; text-align:right; opacity:0.75;">
        Snapshot locale · {created_dt}
    </div>
    """
    content = re.sub(r'<div id="snapshot-banner".*?</div>', '', content, flags=re.S)
    if '</body>' in content:
        return content.replace('</body>', f'{banner}</body>')
    return f'{content}{banner}'


def biblioteca_iframe(request):
    CACHE_KEY = 'biblioteca_iframe_content'
    cached_content = cache.get(CACHE_KEY)
    # Serve a permanent local snapshot if present (no external fetch)
    local_snapshot = os.environ.get('BIBLIOTECA_SNAPSHOT_FILE', '/home/azureuser/IlViale/biblioteca/biblioteca_iframe_snapshot.html')
    if os.path.exists(local_snapshot):
        try:
            with open(local_snapshot, 'r', encoding='utf-8') as f:
                content = f.read()
            content = _inject_snapshot_banner(content, local_snapshot)
            resp = HttpResponse(content, content_type='text/html')
            resp['X-Cache'] = 'SNAPSHOT'
            return resp
        except Exception:
            # If reading snapshot fails, fall back to existing logic
            pass

    if cached_content is None:
        url = "https://mailchi.mp/e4fc2f1a5400/ellida"
        headers = {
            "User-Agent": request.META.get('HTTP_USER_AGENT', ''),
            "Accept-Language": request.META.get('HTTP_ACCEPT_LANGUAGE', ''),
            "Accept": request.META.get('HTTP_ACCEPT', ''),
            "Referer": request.META.get('HTTP_REFERER', ''),
        }

        session = requests.Session()
        session.cookies.clear()
        response = session.get(url, headers=headers)
        content = response.content.decode('utf-8')
        
        # # First remove any existing OG tags
        # soup = BeautifulSoup(content, 'html.parser')
        # for meta in soup.find_all('meta', property=lambda x: x and x.startswith('og:')):
        #     meta.decompose()
        # content = str(soup)

        content = response.text
        content = content.replace(
            'og:',
            'og_removed:'
        )

        # Then perform the image replacement
        content = content.replace(
            'https://mcusercontent.com/ab5e8ed8c9b39209c68db19d5/images/4ebf9ea4-ee9d-71bb-bc9d-19e5ccd727f6.png',
            'https://vialeformica.org/static/images/LogoViale2019_plain.svg'
        )
        
        # Add our Open Graph tags
        og_tags = """
        <meta property="og:type" content="website" />
        <meta property="og:image" content="https://vialeformica.org/static/images/logoassociazione1.jpg" />
        <meta property="og:image:type" content="image/jpeg" />
        <meta property="og:image:width" content="1200" />
        <meta property="og:image:height" content="630" />
        <meta property="og:image:alt" content="Nome associazione con stele di Castionetto" />
        """
        
        # Insert the new OG tags in head
        if '</head>' in content:
            content = content.replace('</head>', f'{og_tags}\n</head>')
        else:
            content = f"<head>{og_tags}</head>\n{content}"

        cache.set(CACHE_KEY, content, timeout=timedelta(minutes=30).total_seconds())
        cache_status = 'MISS'
    else:
        content = cached_content
        cache_status = 'HIT'
    
    response = HttpResponse(content, content_type='text/html')
    response['X-Cache'] = cache_status
    return response

def biblioteca_dona(request):
    return redirect('https://www.provaltellina.org/projects/spazio-ellida-sala-multifunzionale-sostenibile-per-cultura-e-inclusione/')
    #return render(request, 'biblioteca/dona.html')


def provaltellina(request):
    CACHE_KEY = 'provaltellina_content_v4'
    CACHE_TIMESTAMP_KEY = 'provaltellina_last_fetch'
    url = "https://www.provaltellina.org/projects/spazio-ellida-sala-multifunzionale-sostenibile-per-cultura-e-inclusione/"
    FALLBACK_FILE = "/home/azureuser/IlViale/biblioteca/RispostaProValtellina.html"
    CACHE_TIMEOUT = 1800
    INITIAL_TIMEOUT = 5
    RETRY_TIMEOUT = 15
    
    # Debug information container
    debug_info = []
    debug_info.append(f"Starting provaltellina request at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def wrap_response(content, debug_info):
        """Helper to wrap content with debug info (UTF-8 safe)"""
        debug_html = "<div style='background:#f0f0f0;padding:10px;margin:10px;border:1px solid #ccc;'>"
        debug_html += "<h3>Debug Information</h3><ul>"
        
        # Safely encode each debug message
        for msg in debug_info:
            if isinstance(msg, str):
                safe_msg = msg.encode('utf-8', errors='replace').decode('utf-8')
            else:
                safe_msg = str(msg)
            debug_html += f"<li>{safe_msg}</li>"
        
        debug_html += "</ul></div>"
        return content.replace('</body>', f"{debug_html}</body>") if '</body>' in content else content + debug_html

    # 1. Check cache status
    cache_check_start = time.time()
    last_fetch = cache.get(CACHE_TIMESTAMP_KEY)
    current_time = time.time()
    should_refresh = last_fetch is None or (current_time - last_fetch) > CACHE_TIMEOUT
    debug_info.append(f"Cache check completed in {time.time() - cache_check_start:.3f}s (should_refresh={should_refresh}, last_fetch={last_fetch})")
    should_refresh = True
    # 2. Try to fetch fresh content if needed
    if should_refresh:
        debug_info.append("Attempting fresh content fetch")
        try:
            fetch_start = time.time()
            
            # Cookie request
            # cookie_start = time.time()
            # session.get("https://www.provaltellina.org", headers={
            #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            # }, timeout=INITIAL_TIMEOUT)
            # debug_info.append(f"Initial cookie request completed in {time.time() - cookie_start:.3f}s")
            
            # # Random delay
            # delay = random.uniform(1, 3)
            # time.sleep(delay)
            # debug_info.append(f"Waited {delay:.2f}s between requests")
            
            # Main request
            main_start = time.time()
            afd_url = f"{AFD_PROXY_URL}/projects/spazio-ellida-sala-multifunzionale-sostenibile-per-cultura-e-inclusione/"
            response = session.get(
                afd_url,
                headers={
                    "User-Agent": request.META.get('HTTP_USER_AGENT', ''),
                    **AFD_HEADERS
                },
                timeout=10
            )
            #response.encoding = 'utf-8' 
            debug_info.append(f"Main request completed in {time.time() - main_start:.3f}s (status={response.status_code})")
            response.raise_for_status()
            
            # Process content
            process_start = time.time()
            content = response.text
            # Add safe debug info
            try:
                # Find all info-col divs
                info_cols = re.findall(r'<div class="info-col">(.*?)</div>', content, re.DOTALL)
                debug_info.append(f"Found {len(info_cols)} info-col divs")
                
                if len(info_cols) >= 3:
                    # Clean and extract amount from 3rd column
                    amount_text = info_cols[2].strip()
                    debug_info.append(f"Raw amount text: {amount_text[:50]}...")
                    
                    # Extract number with flexible pattern
                    amount_match = re.search(r'([\d.,]+)\s*€', amount_text.replace('&nbsp;', ' '))
                    if amount_match:
                        collected_str = amount_match.group(1).replace('.', '').replace(',', '.')
                        try:
                            collected_amount = float(collected_str)
                            debug_info.append(f"Parsed amount: {collected_amount}€")
                            
                            # Calculate percentage
                            percentage = min(100, max(0, int(round((collected_amount / 4200) * 100))))
                            debug_info.append(f"Calculated percentage: {percentage}%")
                            
                            # Update progress bar
                            #pattern = r'(<div\s+class="progress-bar-number">)[^<]*(</div>)'  
                            
                            start_marker = '<div class="progress-bar">'  
                            end_marker = '</div>'  
                            
                            start_index = content.find(start_marker)  
                            debug_info.append(f"start_index = {start_index}")
                            if start_index != -1:  
                                start_index += len(start_marker)  
                                end_index = content.find(end_marker, start_index)  
                                if end_index != -1:  
                                    # Build the new content  
                                    new_content = (  
                                        content[:start_index] +  
                                        f'''<div class="progress-bar-value ">
                                                <div class="progress-bar-number">{percentage}%</div>      
                                            </div>''' +  
                                        content[end_index:]  
                                    )  
                                    content = new_content  
                        except ValueError as e:
                            debug_info.append(f"Amount parsing failed: {str(e)}")
                    else:
                        debug_info.append("No amount found in 3rd column")
                else:
                    debug_info.append("Not enough info-col divs found")
                    
            except Exception as e:
                tb = sys.exc_info()[2]  
                lineno = tb.tb_lineno  
                debug_info.append(f"({lineno})Amount extraction error: {str(e)}")
                logger.error(f"({lineno})Amount extraction failed: {str(e)}")
            #content = content.replace("2.520", "4.200")
                    #content = content.replace("2.520", "4.200")
                # Add your modifications
            content = content.replace(
                "titolo del progetto e bando di riferimento", 
                "3292 - spazio Ellida"
            ).replace("2.520", "4.200")

            debug_info.append(f"Content processed in {time.time() - process_start:.3f}s")
            
            # Update cache
            cache_start = time.time()
            cache.set(CACHE_KEY, content, CACHE_TIMEOUT)
            cache.set(CACHE_TIMESTAMP_KEY, current_time, CACHE_TIMEOUT * 2)
            debug_info.append(f"Cache updated in {time.time() - cache_start:.3f}s")
            
            debug_info.append(f"Total fetch time: {time.time() - fetch_start:.3f}s")
            safe_debug_info = []
            for item in debug_info:
                if isinstance(item, str):
                    safe_debug_info.append(item.encode('ascii', 'ignore').decode('ascii'))
                else:
                    safe_debug_info.append(str(item))
            
            debug_info = safe_debug_info
            return HttpResponse(wrap_response(content, debug_info), content_type='text/html')
            
        except Exception as e:
            error_msg = f"Initial fetch failed: {str(e)}"
            debug_info.append(error_msg)
            logger.warning(error_msg)
            
            # Launch background refresh
            try:
                threading.Thread(target=async_refresh_content).start()
                debug_info.append("Background refresh started with longer timeout")
                logger.warning("Background refresh started with longer timeout")
            except Exception as e:
                debug_info.append(f"Failed to start background refresh: {str(e)}")
                logger.warning(f"Failed to start background refresh: {str(e)}")

    # 3. Try to serve from cache
    cache_retrieve_start = time.time()
    cached_content = cache.get(CACHE_KEY)
    debug_info.append(f"Cache retrieval took {time.time() - cache_retrieve_start:.3f}s")
    
    if cached_content:
        debug_info.append("Serving from cache")
        return HttpResponse(wrap_response(cached_content, debug_info), content_type='text/html')

    # 4. Fallback to static file
    debug_info.append("No cached content available, trying fallback file")
    try:
        file_start = time.time()
        with open(FALLBACK_FILE, 'r', encoding='utf-8') as f:
            fallback_content = f.read()
            fallback_content = fallback_content.replace("2.520", "4.200")
            debug_info.append(f"Fallback file loaded in {time.time() - file_start:.3f}s")
            return HttpResponse(wrap_response(fallback_content, debug_info), content_type='text/html')
    except Exception as file_error:
        error_msg = f"Failed to read fallback file: {str(file_error)}"
        debug_info.append(error_msg)
        logger.error(error_msg)
        debug_info.append("Returning error response")
        return HttpResponse(wrap_response("Content temporarily unavailable", debug_info), status=503)
        
def provaltellina_prova(request):
    CACHE_KEY = 'provaltellina_content_v4'
    CACHE_TIMESTAMP_KEY = 'provaltellina_last_fetch'
    url = "https://www.provaltellina.org/projects/spazio-ellida-sala-multifunzionale-sostenibile-per-cultura-e-inclusione/"
    FALLBACK_FILE = "/home/azureuser/IlViale/biblioteca/RispostaProValtellina.html"
    CACHE_TIMEOUT = 1800
    INITIAL_TIMEOUT = 5
    RETRY_TIMEOUT = 15
    logging.basicConfig(  
        level=logging.ERROR,  
        format='%(asctime)s %(levelname)s [--%(filename)s:%(lineno)d] %(message)s'  
    )  

    
    # Debug information container
    debug_info = []
    debug_info.append(f"Starting provaltellina request at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.warning("Starting provaltellina request at %s", time.strftime('%Y-%m-%d %H:%M:%S'))
    
    def wrap_response(content, debug_info):
        """Helper to wrap content with debug info (UTF-8 safe)"""
        debug_html = "<div style='background:#f0f0f0;padding:10px;margin:10px;border:1px solid #ccc;display:none;'>"
        debug_html += "<h3>Debug Information</h3><ul>"
        
        # Safely encode each debug message
        for msg in debug_info:
            if isinstance(msg, str):
                safe_msg = msg.encode('utf-8', errors='replace').decode('utf-8')
            else:
                safe_msg = str(msg)
            debug_html += f"<li>{safe_msg}</li>"
        
        debug_html += "</ul></div>"
        return content.replace('</body>', f"{debug_html}</body>") if '</body>' in content else content + debug_html

    # 1. Check cache status
    cache_check_start = time.time()
    last_fetch = cache.get(CACHE_TIMESTAMP_KEY)
    current_time = time.time()
    should_refresh = last_fetch is None or (current_time - last_fetch) > CACHE_TIMEOUT
    debug_info.append(f"Cache check completed in {time.time() - cache_check_start:.3f}s (should_refresh={should_refresh}, last_fetch={last_fetch})")
    logger.warning("Cache check completed in %.3fs (should_refresh=%s, last_fetch=%s)", 
                   time.time() - cache_check_start, 
                   should_refresh, 
                   last_fetch)
    # For testing purposes, force refresh
    #
    #should_refresh = True
    # 2. Try to fetch fresh content if needed
    if should_refresh:
        debug_info.append("Attempting fresh content fetch")
 
        try:
            fetch_start = time.time()
            
            # Cookie request
            # cookie_start = time.time()
            # session.get("https://www.provaltellina.org", headers={
            #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            # }, timeout=INITIAL_TIMEOUT)
            # debug_info.append(f"Initial cookie request completed in {time.time() - cookie_start:.3f}s")
            
            # # Random delay
            # delay = random.uniform(1, 3)
            # time.sleep(delay)
            # debug_info.append(f"Waited {delay:.2f}s between requests")
            
            # Main request
            main_start = time.time()
            afd_url = f"{AFD_PROXY_URL}/projects/spazio-ellida-sala-multifunzionale-sostenibile-per-cultura-e-inclusione/"
            response = session.get(
                afd_url,
                headers={
                    "User-Agent": request.META.get('HTTP_USER_AGENT', ''),
                    **AFD_HEADERS
                },
                timeout=10
            )
            response.encoding = 'utf-8' 
            debug_info.append(f"Main request completed in {time.time() - main_start:.3f}s (status={response.status_code})")
            response.raise_for_status()
            
            # Process content
            process_start = time.time()
            #response.encoding = 'utf-8'  # Explicitly set encoding
            content = response.text
            # Add safe debug info
            try:
                # Find all info-col divs
                info_cols = re.findall(r'<div class="info-col">(.*?)</div>', content, re.DOTALL)
                debug_info.append(f"Found {len(info_cols)} info-col divs")
                
                if len(info_cols) >= 3:
                    # Clean and extract amount from 3rd column
                    amount_text = info_cols[2].strip()
                    debug_info.append(f"Raw amount text: {amount_text[:50]}...")
                    
                    # Extract number with flexible pattern
                    amount_match = re.search(r'([\d.,]+)\s*€', amount_text.replace('&nbsp;', ' '))
                    if amount_match:
                        collected_str = amount_match.group(1).replace('.', '').replace(',', '.')
                        try:
                            collected_amount = float(collected_str)
                            debug_info.append(f"Parsed amount: {collected_amount}€")
                            
                            # Calculate percentage
                            percentage = min(100, max(0, int(round((collected_amount / 4200) * 100))))
                            debug_info.append(f"Calculated percentage: {percentage}%")
                            
                            # Update progress bar
                            #pattern = r'(<div\s+class="progress-bar-number">)[^<]*(</div>)'  
                            
                            start_marker = '<div class="progress-bar">'  
                            end_marker = '</div>'  
                            
                            start_index = content.find(start_marker)  
                            debug_info.append(f"start_index = {start_index}")
                            if start_index != -1:  
                                start_index += len(start_marker)  
                                end_index = content.find(end_marker, start_index)  
                                if end_index != -1:  
                                    # Build the new content  
                                    new_content = (  
                                        content[:start_index] +  
                                        f'''<div class="progress-bar-value ">
                                                <div class="progress-bar-number">{percentage}%''' +  
                                        content[end_index:]  
                                    )  
                                    content = new_content  
                        except ValueError as e:
                            debug_info.append(f"Amount parsing failed: {str(e)}")
                    else:
                        debug_info.append("No amount found in 3rd column")
                else:
                    debug_info.append("Not enough info-col divs found")
                    
            except Exception as e:
                tb = sys.exc_info()[2]  
                lineno = tb.tb_lineno  
                debug_info.append(f"({lineno})Amount extraction error: {str(e)}")
                logger.error(f"({lineno})Amount extraction failed: {str(e)}")
            #content = content.replace("2.520", "4.200")
                    #content = content.replace("2.520", "4.200")
                # Add your modifications
            content = content.replace(
                "titolo del progetto e bando di riferimento", 
                "3292 - spazio Ellida"
            )#.replace("2.520", "4.200")

            debug_info.append(f"Content processed in {time.time() - process_start:.3f}s")
            
            # Update cache
            cache_start = time.time()
            cache.set(CACHE_KEY, content, CACHE_TIMEOUT)
            cache.set(CACHE_TIMESTAMP_KEY, current_time, CACHE_TIMEOUT * 2)
            debug_info.append(f"Cache updated in {time.time() - cache_start:.3f}s")
            
            debug_info.append(f"Total fetch time: {time.time() - fetch_start:.3f}s")
            safe_debug_info = []
            for item in debug_info:
                if isinstance(item, str):
                    safe_debug_info.append(item.encode('ascii', 'ignore').decode('ascii'))
                else:
                    safe_debug_info.append(str(item))
            
            debug_info = safe_debug_info
            debug_info.append(f"return HttpResponse")
            return HttpResponse(wrap_response(content, debug_info), content_type='text/html')
            
        except Exception as e:
            error_msg = f"Initial fetch failed: {str(e)}"
            debug_info.append(error_msg)
            logger.warning(error_msg)
            
            # Launch background refresh
            try:
                threading.Thread(target=async_refresh_content).start()
                debug_info.append("Background refresh started with longer timeout")
                logger.warning("Background refresh started with longer timeout")
            except Exception as e:
                debug_info.append(f"Failed to start background refresh: {str(e)}")
                logger.warning(f"Failed to start background refresh: {str(e)}")

    # 3. Try to serve from cache
    cache_retrieve_start = time.time()
    cached_content = cache.get(CACHE_KEY)
    debug_info.append(f"Cache retrieval took {time.time() - cache_retrieve_start:.3f}s")
    
    if cached_content:
        debug_info.append("Serving from cache")
        return HttpResponse(wrap_response(cached_content, debug_info), content_type='text/html')

    # 4. Fallback to static file
    debug_info.append("No cached content available, trying fallback file")
    try:
        file_start = time.time()
        with open(FALLBACK_FILE, 'r', encoding='utf-8') as f:
            fallback_content = f.read()
            fallback_content = fallback_content.replace("2.520", "4.200")
            debug_info.append(f"Fallback file loaded in {time.time() - file_start:.3f}s")
            return HttpResponse(wrap_response(fallback_content, debug_info), content_type='text/html')
    except Exception as file_error:
        error_msg = f"Failed to read fallback file: {str(file_error)}"
        debug_info.append(error_msg)
        logger.error(error_msg)
        debug_info.append("Returning error response")
        return HttpResponse(wrap_response("Content temporarily unavailable", debug_info), status=503)