from flask import Flask, request, render_template, jsonify
import requests
import os
from PIL import Image
import io
import json
import base64
import re
from datetime import datetime
import math
from collections import Counter

app = Flask(__name__)

VISION_API_KEY = "AIzaSyBzlDMMAs7WXVohoYhss60xY1DImVX5l7o"

def calculate_similarity_metrics(search_results):
    # ...existing code...
    if not search_results:
        return {
            'similarity_score': 0,
            'scam_probability': 'Low',
            'confidence': 'High',
            'reasons': ['Image appears to be unique - low scam risk']
        }
    exact_matches = [r for r in search_results if r.get('type') == 'exact_match']
    page_matches = [r for r in search_results if r.get('type') == 'page_match']
    similar_matches = [r for r in search_results if r.get('type') == 'similar_match']
    total_matches = len(exact_matches) + len(page_matches) + len(similar_matches)
    exact_score = len(exact_matches) * 10
    page_score = len(page_matches) * 7
    similar_score = len(similar_matches) * 3
    total_score = exact_score + page_score + similar_score
    similarity_score = min(100, total_score * 2)
    if similarity_score >= 70:
        scam_prob = "High"
        confidence = "High" if len(exact_matches) > 3 else "Medium"
    elif similarity_score >= 30:
        scam_prob = "Medium"
        confidence = "Medium"
    else:
        scam_prob = "Low"
        confidence = "High"
    reasons = []
    if exact_matches:
        reasons.append(f"Found {len(exact_matches)} exact matches online")
    if page_matches:
        reasons.append(f"Appears on {len(page_matches)} different web pages")
    if similar_matches:
        reasons.append(f"Has {len(similar_matches)} visually similar images")
    if not reasons:
        reasons = ["No significant matches found - likely authentic"]
    return {
        'similarity_score': round(similarity_score),
        'scam_probability': scam_prob,
        'confidence': confidence,
        'total_matches': total_matches,
        'reasons': reasons,
        'breakdown': {
            'exact_matches': len(exact_matches),
            'page_matches': len(page_matches),
            'similar_matches': len(similar_matches)
        }
    }

def analyze_domain_patterns(search_results):
    domains = []
    for result in search_results:
        if result.get('link'):
            try:
                from urllib.parse import urlparse
                domain = urlparse(result['link']).netloc
                domains.append(domain)
            except:
                pass
    domain_counts = Counter(domains)
    suspicious_domains = []
    scam_indicators = ['classified', 'ads', 'listing', 'rental', 'sale', 'offer']
    for domain, count in domain_counts.most_common():
        if any(indicator in domain.lower() for indicator in scam_indicators):
            suspicious_domains.append(domain)
    return {
        'unique_domains': len(domain_counts),
        'suspicious_domains': suspicious_domains,
        'domain_distribution': dict(domain_counts.most_common(5))
    }

def estimate_date_from_url(url):
    try:
        date_patterns = [
            r'/(\d{4})/(\d{1,2})/(\d{1,2})/',
            r'/(\d{4})-(\d{1,2})-(\d{1,2})/',
            r'/(\d{4})(\d{2})(\d{2})/',
            r'(\d{4})/(\d{2})/(\d{2})',
        ]
        for pattern in date_patterns:
            match = re.search(pattern, url)
            if match:
                groups = match.groups()
                if len(groups) == 3:
                    year, month, day = groups
                    datetime(int(year), int(month), int(day))
                    return f"Estimated: {year}-{month}-{day}"
        year_match = re.search(r'/(\d{4})/', url)
        if year_match:
            return f"Estimated year: {year_match.group(1)}"
    except:
        pass
    return "Date unknown"

def reverse_image_search(image_data):
    try:
        if not image_data or len(image_data) == 0:
            print("❌ Error: Empty image data received")
            return []
        print(f"✅ Received image data: {len(image_data)} bytes")
        encoded_image = base64.b64encode(image_data).decode('utf-8')
        api_url = f"https://vision.googleapis.com/v1/images:annotate?key={VISION_API_KEY}"
        request_body = {
            "requests": [
                {
                    "image": {"content": encoded_image},
                    "features": [{"type": "WEB_DETECTION", "maxResults": 10}]
                }
            ]
        }
        response = requests.post(api_url, json=request_body, timeout=30)
        if response.status_code != 200:
            print(f"❌ API returned status code: {response.status_code}")
            return []
        result = response.json()
        if "responses" in result and result["responses"]:
            if "error" in result["responses"][0]:
                error = result["responses"][0]["error"]
                print(f"❌ Vision API error: {error.get('message')}")
                return []
        search_results = []
        if "responses" in result and result["responses"]:
            web_detection = result["responses"][0].get("webDetection", {})
            best_guess_labels = []
            if web_detection.get("bestGuessLabels"):
                for label in web_detection["bestGuessLabels"]:
                    best_guess_labels.append(label.get("label", ""))
            web_entities = []
            if web_detection.get("webEntities"):
                for entity in web_detection["webEntities"]:
                    if entity.get("description"):
                        web_entities.append({
                            "description": entity.get("description"),
                            "score": entity.get("score", 0)
                        })
            if web_detection.get("fullMatchingImages"):
                for img in web_detection["fullMatchingImages"][:5]:
                    url = img.get('url', '')
                    result_entry = {
                        'type': 'exact_match',
                        'title': 'Exact Match Found',
                        'link': url,
                        'details': {
                            'match_type': 'Exact duplicate',
                            'confidence': 'High',
                            'image_size': f"{img.get('width', 'Unknown')}x{img.get('height', 'Unknown')}" if img.get('width') else 'Unknown',
                            'estimated_date': estimate_date_from_url(url)
                        }
                    }
                    search_results.append(result_entry)
            if web_detection.get("pagesWithMatchingImages"):
                for page in web_detection["pagesWithMatchingImages"][:5]:
                    url = page.get('url', '')
                    result_entry = {
                        'type': 'page_match',
                        'title': f"Page: {page.get('pageTitle', 'Unknown page')}",
                        'link': url,
                        'details': {
                            'match_type': 'Page containing this image',
                            'page_title': page.get('pageTitle', 'Unknown'),
                            'context': 'Website page where this image appears',
                            'estimated_date': estimate_date_from_url(url)
                        }
                    }
                    search_results.append(result_entry)
            if web_detection.get("visuallySimilarImages"):
                for img in web_detection["visuallySimilarImages"][:5]:
                    url = img.get('url', '')
                    result_entry = {
                        'type': 'similar_match',
                        'title': 'Visually Similar Image',
                        'link': url,
                        'details': {
                            'match_type': 'Visually similar content',
                            'confidence': 'Medium',
                            'image_size': f"{img.get('width', 'Unknown')}x{img.get('height', 'Unknown')}" if img.get('width') else 'Unknown',
                            'estimated_date': estimate_date_from_url(url)
                        }
                    }
                    search_results.append(result_entry)
            if best_guess_labels or web_entities:
                context_info = {
                    'type': 'analysis',
                    'title': 'Image Analysis Results',
                    'link': '',
                    'details': {
                        'best_guess_labels': best_guess_labels,
                        'related_concepts': [entity['description'] for entity in web_entities[:3]],
                        'analysis_note': 'Based on Google AI analysis of image content'
                    }
                }
                search_results.append(context_info)
        print(f"✅ Search completed. Found {len(search_results)} results")
        return search_results
    except Exception as e:
        print(f"❌ Error during reverse search: {e}")
        import traceback
        traceback.print_exc()
        return []

def track_scan_activity(ip_address, filename, result_count, risk_level):
    try:
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'ip': ip_address,
            'filename': filename,
            'result_count': result_count,
            'risk_level': risk_level
        }
        print(f"SCAN_ACTIVITY: {json.dumps(log_entry)}")
    except Exception as e:
        print(f"Analytics error: {e}")

def get_image_metadata(image_data):
    try:
        image = Image.open(io.BytesIO(image_data))
        metadata = {
            "format": image.format,
            "mode": image.mode,
            "size": image.size,
            "info": image.info
        }
        return metadata
    except Exception as e:
        print(f"Error extracting metadata: {e}")
        return {}
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    try:
        image_data = file.read()
        if not image_data or len(image_data) == 0:
            return jsonify({'error': 'File is empty or corrupted'}), 400
        print(f"📸 File uploaded: {file.filename}, Size: {len(image_data)} bytes")
        metadata = get_image_metadata(image_data)
        reverse_search_results = reverse_image_search(image_data)
        similarity_metrics = calculate_similarity_metrics(reverse_search_results)
        domain_analysis = analyze_domain_patterns(reverse_search_results)
        scam_report = generate_scam_report(similarity_metrics, domain_analysis)
        track_scan_activity(
            ip_address=request.remote_addr,
            filename=file.filename,
            result_count=len(reverse_search_results),
            risk_level=scam_report['risk_level']
        )
        result = {
            'metadata': metadata,
            'reverseSearchResults': reverse_search_results,
            'similarity_metrics': similarity_metrics,
            'domain_analysis': domain_analysis,
            'scam_report': scam_report,
            'summary': generate_summary(similarity_metrics, scam_report),
            'timestamp': datetime.now().isoformat()
        }
        return jsonify(result)
    except Exception as e:
        print(f"❌ Error in scan route: {e}")
        return jsonify({'error': 'Server error processing image'}), 500

def generate_scam_report(metrics, domains):
    score = metrics['similarity_score']
    probability = metrics['scam_probability']
    report = {
        'risk_level': probability,
        'risk_score': score,
        'recommendation': '',
        'warning_level': 'green'
    }
    if probability == "High":
        report['recommendation'] = "⚠️ HIGH RISK: This image appears in multiple locations. Exercise extreme caution."
        report['warning_level'] = 'red'
    elif probability == "Medium":
        report['recommendation'] = "⚠️ MEDIUM RISK: This image may be reused. Verify carefully."
        report['warning_level'] = 'yellow'
    else:
        report['recommendation'] = "✅ LOW RISK: This image appears unique. Likely authentic."
        report['warning_level'] = 'green'
    if domains['suspicious_domains']:
        report['recommendation'] += f" Found on {len(domains['suspicious_domains'])} suspicious domains."
    return report

def generate_summary(metrics, scam_report):
    return {
        'verdict': scam_report['risk_level'],
        'confidence': metrics['confidence'],
        'quick_advice': scam_report['recommendation'],
        'match_count': metrics['total_matches']
    }

if __name__ == '__main__':
    app.run(debug=True)