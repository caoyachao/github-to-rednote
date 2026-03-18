#!/usr/bin/env python3
"""
RedNote (小红书) Cover Image Generator
Generate 1080x1440 cover images for GitHub repository promotion.
Uses canvas tool for image generation.
"""

import os
import sys
import json
import tempfile
import subprocess
from pathlib import Path
from typing import Optional, Dict

# Canvas tool will be called via exec/invoke

# RedNote standard cover size
COVER_WIDTH = 1080
COVER_HEIGHT = 1440

# Color schemes for different languages/tech stacks
COLOR_SCHEMES = {
    'python': {'bg': '#306998', 'accent': '#FFD43B', 'text': '#FFFFFF'},
    'javascript': {'bg': '#F7DF1E', 'accent': '#323330', 'text': '#323330'},
    'typescript': {'bg': '#3178C6', 'accent': '#FFFFFF', 'text': '#FFFFFF'},
    'go': {'bg': '#00ADD8', 'accent': '#CE3262', 'text': '#FFFFFF'},
    'rust': {'bg': '#CE422B', 'accent': '#000000', 'text': '#FFFFFF'},
    'java': {'bg': '#007396', 'accent': '#F8981D', 'text': '#FFFFFF'},
    'cpp': {'bg': '#00599C', 'accent': '#FFFFFF', 'text': '#FFFFFF'},
    'c': {'bg': '#A8B9CC', 'accent': '#283593', 'text': '#283593'},
    'ruby': {'bg': '#CC342D', 'accent': '#FFFFFF', 'text': '#FFFFFF'},
    'php': {'bg': '#777BB4', 'accent': '#000000', 'text': '#FFFFFF'},
    'swift': {'bg': '#F05138', 'accent': '#FFFFFF', 'text': '#FFFFFF'},
    'kotlin': {'bg': '#7F52FF', 'accent': '#FFFFFF', 'text': '#FFFFFF'},
    'default': {'bg': '#1a1a2e', 'accent': '#e94560', 'text': '#FFFFFF'}
}


def get_color_scheme(language: Optional[str]) -> Dict[str, str]:
    """Get color scheme based on programming language."""
    if not language:
        return COLOR_SCHEMES['default']
    
    lang_lower = language.lower()
    
    # Map common variations
    lang_map = {
        'python': 'python',
        'javascript': 'javascript', 'js': 'javascript',
        'typescript': 'typescript', 'ts': 'typescript',
        'go': 'go', 'golang': 'go',
        'rust': 'rust',
        'java': 'java',
        'c++': 'cpp', 'cpp': 'cpp',
        'c': 'c',
        'ruby': 'ruby',
        'php': 'php',
        'swift': 'swift',
        'kotlin': 'kotlin'
    }
    
    mapped = lang_map.get(lang_lower, 'default')
    return COLOR_SCHEMES.get(mapped, COLOR_SCHEMES['default'])


def format_stars(stars: int) -> str:
    """Format stars count for display."""
    if stars >= 1000:
        return f"{stars/1000:.1f}k"
    elif stars >= 100:
        return str(stars)
    return ""


def should_show_stars(stars: int) -> bool:
    """Check if stars should be displayed (>= 100)."""
    return stars >= 100


def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text to max length."""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def generate_cover_js(repo_data: dict, output_path: str) -> str:
    """
    Generate JavaScript code for canvas cover image.
    Returns the JS code that can be executed via canvas tool.
    """
    colors = get_color_scheme(repo_data.get('language'))
    
    repo_name = repo_data.get('repo', 'Unknown')
    description = truncate_text(repo_data.get('description', ''), 60)
    language = repo_data.get('language', 'Unknown') or 'Unknown'
    stars = repo_data.get('stars', 0)
    
    # Truncate repo name if too long
    display_name = truncate_text(repo_name, 20)
    
    # Stars display logic
    stars_badge = ""
    if should_show_stars(stars):
        stars_formatted = format_stars(stars)
        stars_badge = f"⭐ {stars_formatted} stars"
    
    js_code = f"""
const canvas = document.createElement('canvas');
canvas.width = {COVER_WIDTH};
canvas.height = {COVER_HEIGHT};
const ctx = canvas.getContext('2d');

// Background - tech gradient
const gradient = ctx.createLinearGradient(0, 0, {COVER_WIDTH}, {COVER_HEIGHT});
gradient.addColorStop(0, '{colors['bg']}');
gradient.addColorStop(0.5, '#16213e');
gradient.addColorStop(1, '#0f0f23');
ctx.fillStyle = gradient;
ctx.fillRect(0, 0, {COVER_WIDTH}, {COVER_HEIGHT});

// Grid pattern overlay
ctx.strokeStyle = 'rgba(255,255,255,0.03)';
ctx.lineWidth = 1;
for (let i = 0; i < {COVER_WIDTH}; i += 40) {{
    ctx.beginPath();
    ctx.moveTo(i, 0);
    ctx.lineTo(i, {COVER_HEIGHT});
    ctx.stroke();
}}
for (let i = 0; i < {COVER_HEIGHT}; i += 40) {{
    ctx.beginPath();
    ctx.moveTo(0, i);
    ctx.lineTo({COVER_WIDTH}, i);
    ctx.stroke();
}}

// Accent line at top
ctx.fillStyle = '{colors['accent']}';
ctx.fillRect(60, 80, 120, 6);

// GitHub Icon (simplified)
ctx.fillStyle = 'rgba(255,255,255,0.1)';
ctx.beginPath();
ctx.arc(180, 220, 80, 0, Math.PI * 2);
ctx.fill();

// GitHub cat silhouette
ctx.fillStyle = '{colors['accent']}';
ctx.beginPath();
ctx.arc(180, 230, 50, 0, Math.PI * 2);
ctx.fill();
ctx.fillStyle = '{colors['bg']}';
ctx.beginPath();
ctx.arc(180, 240, 35, 0, Math.PI * 2);
ctx.fill();

// Main title
ctx.fillStyle = '{colors['text']}';
ctx.font = 'bold 72px "PingFang SC", "Microsoft YaHei", sans-serif';
ctx.textAlign = 'center';
ctx.fillText('{display_name}', {COVER_WIDTH/2}, 450);

// Description
ctx.fillStyle = 'rgba(255,255,255,0.85)';
ctx.font = '32px "PingFang SC", "Microsoft YaHei", sans-serif';
ctx.textAlign = 'center';

// Word wrap for description
const desc = '{description}';
const maxWidth = 900;
const words = desc.split('');
let line = '';
let y = 540;
for (let i = 0; i < words.length; i++) {{
    const testLine = line + words[i];
    const metrics = ctx.measureText(testLine);
    if (metrics.width > maxWidth && i > 0) {{
        ctx.fillText(line, {COVER_WIDTH/2}, y);
        line = words[i];
        y += 50;
    }} else {{
        line = testLine;
    }}
}}
ctx.fillText(line, {COVER_WIDTH/2}, y);

// Tech badge
ctx.fillStyle = '{colors['accent']}';
ctx.roundRect({COVER_WIDTH/2 - 100}, 700, 200, 50, 25);
ctx.fill();
ctx.fillStyle = '{colors['bg'] if colors['text'] == '#FFFFFF' else colors['text']}';
ctx.font = 'bold 24px "PingFang SC", sans-serif';
ctx.textAlign = 'center';
ctx.fillText('{language}', {COVER_WIDTH/2}, 733);

// Stars badge (if >= 100)
{'// Stars badge' if stars_badge else '// No stars badge'}
{'ctx.fillStyle = "#FFD700";' if stars_badge else ''}
{'ctx.roundRect(390, 780, 300, 60, 30);' if stars_badge else ''}
{'ctx.fill();' if stars_badge else ''}
{'ctx.fillStyle = "#1a1a2e";' if stars_badge else ''}
{'ctx.font = "bold 28px sans-serif";' if stars_badge else ''}
{f'ctx.fillText("{stars_badge}", 540, 820);' if stars_badge else ''}

// Bottom section - tech decoration
ctx.strokeStyle = '{colors['accent']}';
ctx.lineWidth = 3;
ctx.beginPath();
ctx.moveTo(60, {COVER_HEIGHT - 200});
ctx.lineTo({COVER_WIDTH - 60}, {COVER_HEIGHT - 200});
ctx.stroke();

// Code-like decoration
ctx.fillStyle = 'rgba(255,255,255,0.15)';
ctx.font = '24px "Courier New", monospace';
ctx.textAlign = 'left';
ctx.fillText('const awesome = true;', 80, {COVER_HEIGHT - 140});
ctx.fillText('// Open Source', 80, {COVER_HEIGHT - 100});
ctx.fillText('#GitHub #OpenSource', 80, {COVER_HEIGHT - 60});

// Corner decoration
ctx.fillStyle = '{colors['accent']}';
ctx.beginPath();
ctx.arc({COVER_WIDTH - 100}, {COVER_HEIGHT - 100}, 40, 0, Math.PI * 2);
ctx.fill();
ctx.fillStyle = '{colors['bg']}';
ctx.beginPath();
ctx.arc({COVER_WIDTH - 100}, {COVER_HEIGHT - 100}, 25, 0, Math.PI * 2);
ctx.fill();

// Export
return canvas.toDataURL('image/png');
"""
    return js_code


def generate_cover_image(repo_data: dict, output_dir: str = ".") -> Optional[str]:
    """
    Generate RedNote cover image for a GitHub repository.
    
    Args:
        repo_data: Repository data dictionary
        output_dir: Directory to save the image
    
    Returns:
        Path to the generated image file, or None if generation failed
    """
    import subprocess
    
    repo_name = repo_data.get('repo', 'unknown')
    output_path = os.path.join(output_dir, f"{repo_name}_cover.png")
    
    # Generate JavaScript code for the canvas
    js_code = generate_cover_js(repo_data, output_path)
    
    # Create a temporary HTML file to render the canvas
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ margin: 0; padding: 0; background: #000; }}
        canvas {{ display: block; }}
    </style>
</head>
<body>
    <script>
        {js_code}
        // Save to file by creating a download link
        const dataURL = canvas.toDataURL('image/png');
        const link = document.createElement('a');
        link.download = '{repo_name}_cover.png';
        link.href = dataURL;
        document.body.appendChild(link);
        link.click();
        
        // Also output to console for extraction
        console.log('CANVAS_DATA_URL_START');
        console.log(dataURL);
        console.log('CANVAS_DATA_URL_END');
    </script>
</body>
</html>"""
    
    # Write HTML to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
        f.write(html_content)
        html_path = f.name
    
    try:
        # Use canvas tool to generate the image
        # First try using the canvas snapshot approach
        canvas_js = js_code.replace("return canvas.toDataURL('image/png');", "")
        canvas_js += f"""
// Save to output
const fs = require('fs');
const data = canvas.toDataURL('image/png').replace(/^data:image\\/png;base64,/, '');
fs.writeFileSync('{output_path}', Buffer.from(data, 'base64'));
console.log('Image saved to: {output_path}');
"""
        
        # Alternative: Use Node.js with node-canvas
        node_script = f"""const {{ createCanvas }} = require('canvas');
const fs = require('fs');

const canvas = createCanvas({COVER_WIDTH}, {COVER_HEIGHT});
const ctx = canvas.getContext('2d');

{js_code.replace("const canvas = document.createElement('canvas');", "")
 .replace("canvas.width = {COVER_WIDTH};", "")
 .replace("canvas.height = {COVER_HEIGHT};", "")
 .replace("const ctx = canvas.getContext('2d');", "")}

const buffer = canvas.toBuffer('image/png');
fs.writeFileSync('{output_path}', buffer);
console.log('Saved to {output_path}');
"""
        
        # Try simple approach: generate SVG instead
        return generate_svg_cover(repo_data, output_path)
        
    finally:
        # Cleanup
        try:
            os.unlink(html_path)
        except:
            pass
    
    return None


def generate_svg_cover(repo_data: dict, output_path: str) -> Optional[str]:
    """
    Generate SVG cover image as fallback.
    Returns the path to saved image (converted to PNG).
    """
    colors = get_color_scheme(repo_data.get('language'))
    
    repo_name = repo_data.get('repo', 'Unknown')
    description = truncate_text(repo_data.get('description', ''), 60)
    language = repo_data.get('language', 'Unknown') or 'Unknown'
    stars = repo_data.get('stars', 0)
    
    display_name = truncate_text(repo_name, 20)
    
    # Stars display logic
    stars_badge = ""
    stars_y_offset = 0
    if should_show_stars(stars):
        stars_formatted = format_stars(stars)
        stars_badge = f"⭐ {stars_formatted} stars"
        stars_y_offset = 80
    
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{COVER_WIDTH}" height="{COVER_HEIGHT}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{colors['bg']};stop-opacity:1" />
      <stop offset="50%" style="stop-color:#16213e;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#0f0f23;stop-opacity:1" />
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  
  <!-- Background -->
  <rect width="100%" height="100%" fill="url(#bgGrad)"/>
  
  <!-- Grid pattern -->
  <g stroke="rgba(255,255,255,0.03)" stroke-width="1">
    <line x1="40" y1="0" x2="40" y2="1440"/>
    <line x1="80" y1="0" x2="80" y2="1440"/>
    <line x1="120" y1="0" x2="120" y2="1440"/>
    <line x1="160" y1="0" x2="160" y2="1440"/>
    <line x1="200" y1="0" x2="200" y2="1440"/>
    <line x1="240" y1="0" x2="240" y2="1440"/>
    <line x1="280" y1="0" x2="280" y2="1440"/>
    <line x1="320" y1="0" x2="320" y2="1440"/>
    <line x1="360" y1="0" x2="360" y2="1440"/>
    <line x1="400" y1="0" x2="400" y2="1440"/>
    <line x1="440" y1="0" x2="440" y2="1440"/>
    <line x1="480" y1="0" x2="480" y2="1440"/>
    <line x1="520" y1="0" x2="520" y2="1440"/>
    <line x1="560" y1="0" x2="560" y2="1440"/>
    <line x1="600" y1="0" x2="600" y2="1440"/>
    <line x1="640" y1="0" x2="640" y2="1440"/>
    <line x1="680" y1="0" x2="680" y2="1440"/>
    <line x1="720" y1="0" x2="720" y2="1440"/>
    <line x1="760" y1="0" x2="760" y2="1440"/>
    <line x1="800" y1="0" x2="800" y2="1440"/>
    <line x1="840" y1="0" x2="840" y2="1440"/>
    <line x1="880" y1="0" x2="880" y2="1440"/>
    <line x1="920" y1="0" x2="920" y2="1440"/>
    <line x1="960" y1="0" x2="960" y2="1440"/>
    <line x1="1000" y1="0" x2="1000" y2="1440"/>
    <line x1="1040" y1="0" x2="1040" y2="1440"/>
    <line x1="0" y1="40" x2="1080" y2="40"/>
    <line x1="0" y1="80" x2="1080" y2="80"/>
    <line x1="0" y1="120" x2="1080" y2="120"/>
    <line x1="0" y1="160" x2="1080" y2="160"/>
    <line x1="0" y1="200" x2="1080" y2="200"/>
    <line x1="0" y1="240" x2="1080" y2="240"/>
    <line x1="0" y1="280" x2="1080" y2="280"/>
    <line x1="0" y1="320" x2="1080" y2="320"/>
    <line x1="0" y1="360" x2="1080" y2="360"/>
    <line x1="0" y1="400" x2="1080" y2="400"/>
    <line x1="0" y1="440" x2="1080" y2="440"/>
    <line x1="0" y1="480" x2="1080" y2="480"/>
    <line x1="0" y1="520" x2="1080" y2="520"/>
    <line x1="0" y1="560" x2="1080" y2="560"/>
    <line x1="0" y1="600" x2="1080" y2="600"/>
    <line x1="0" y1="640" x2="1080" y2="640"/>
    <line x1="0" y1="680" x2="1080" y2="680"/>
    <line x1="0" y1="720" x2="1080" y2="720"/>
    <line x1="0" y1="760" x2="1080" y2="760"/>
    <line x1="0" y1="800" x2="1080" y2="800"/>
    <line x1="0" y1="840" x2="1080" y2="840"/>
    <line x1="0" y1="880" x2="1080" y2="880"/>
    <line x1="0" y1="920" x2="1080" y2="920"/>
    <line x1="0" y1="960" x2="1080" y2="960"/>
    <line x1="0" y1="1000" x2="1080" y2="1000"/>
    <line x1="0" y1="1040" x2="1080" y2="1040"/>
    <line x1="0" y1="1080" x2="1080" y2="1080"/>
    <line x1="0" y1="1120" x2="1080" y2="1120"/>
    <line x1="0" y1="1160" x2="1080" y2="1160"/>
    <line x1="0" y1="1200" x2="1080" y2="1200"/>
    <line x1="0" y1="1240" x2="1080" y2="1240"/>
    <line x1="0" y1="1280" x2="1080" y2="1280"/>
    <line x1="0" y1="1320" x2="1080" y2="1320"/>
    <line x1="0" y1="1360" x2="1080" y2="1360"/>
    <line x1="0" y1="1400" x2="1080" y2="1400"/>
  </g>
  
  <!-- Accent line -->
  <rect x="60" y="80" width="120" height="6" fill="{colors['accent']}"/>
  
  <!-- GitHub icon circle -->
  <circle cx="180" cy="220" r="80" fill="rgba(255,255,255,0.1)"/>
  <circle cx="180" cy="230" r="50" fill="{colors['accent']}"/>
  <circle cx="180" cy="240" r="35" fill="{colors['bg']}"/>
  
  <!-- Repo name -->
  <text x="540" y="450" font-family="PingFang SC, Microsoft YaHei, sans-serif" 
        font-size="72" font-weight="bold" fill="{colors['text']}" text-anchor="middle">
    {display_name}
  </text>
  
  <!-- Description -->
  <text x="540" y="540" font-family="PingFang SC, Microsoft YaHei, sans-serif" 
        font-size="32" fill="rgba(255,255,255,0.85)" text-anchor="middle">
    {description}
  </text>
  
  <!-- Language badge -->
  <rect x="440" y="700" width="200" height="50" rx="25" fill="{colors['accent']}"/>
  <text x="540" y="733" font-family="PingFang SC, sans-serif" font-size="24" 
        font-weight="bold" fill="{'#1a1a2e' if colors['text'] == '#FFFFFF' else colors['text']}" text-anchor="middle">
    {language}
  </text>
  
  <!-- Stars badge (conditional) -->
  {'<rect x="390" y="780" width="300" height="60" rx="30" fill="#FFD700"/>' if stars_badge else ''}
  {'<text x="540" y="820" font-family="sans-serif" font-size="28" font-weight="bold" fill="#1a1a2e" text-anchor="middle">' + stars_badge + '</text>' if stars_badge else ''}
  
  <!-- Bottom decoration line -->
  <line x1="60" y1="{1240 + stars_y_offset}" x2="1020" y2="{1240 + stars_y_offset}" 
        stroke="{colors['accent']}" stroke-width="3"/>
  
  <!-- Code decoration -->
  <text x="80" y="{1300 + stars_y_offset}" font-family="Courier New, monospace" 
        font-size="24" fill="rgba(255,255,255,0.15)">const awesome = true;</text>
  <text x="80" y="{1340 + stars_y_offset}" font-family="Courier New, monospace" 
        font-size="24" fill="rgba(255,255,255,0.15)">// Open Source</text>
  <text x="80" y="{1380 + stars_y_offset}" font-family="Courier New, monospace" 
        font-size="24" fill="rgba(255,255,255,0.15)">#GitHub #OpenSource</text>
  
  <!-- Corner decoration -->
  <circle cx="980" cy="{1340 + stars_y_offset}" r="40" fill="{colors['accent']}"/>
  <circle cx="980" cy="{1340 + stars_y_offset}" r="25" fill="{colors['bg']}"/>
</svg>'''
    
    # Save SVG
    svg_path = output_path.replace('.png', '.svg')
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    # Convert SVG to PNG using available tools
    try:
        # Try using cairosvg
        import cairosvg
        cairosvg.svg2png(url=svg_path, write_to=output_path, 
                        output_width=COVER_WIDTH, output_height=COVER_HEIGHT)
        os.unlink(svg_path)  # Remove SVG after conversion
        return output_path
    except ImportError:
        pass
    
    # Try using ImageMagick convert
    try:
        result = subprocess.run(
            ['convert', '-background', 'none', svg_path, 
             '-resize', f'{COVER_WIDTH}x{COVER_HEIGHT}', output_path],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            os.unlink(svg_path)
            return output_path
    except (subprocess.SubprocessError, FileNotFoundError):
        pass
    
    # Try using Inkscape
    try:
        result = subprocess.run(
            ['inkscape', svg_path, '--export-type=png', 
             f'--export-filename={output_path}',
             f'--export-width={COVER_WIDTH}', f'--export-height={COVER_HEIGHT}'],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            os.unlink(svg_path)
            return output_path
    except (subprocess.SubprocessError, FileNotFoundError):
        pass
    
    # Fallback: return SVG path
    print(f"  PNG conversion unavailable, saved SVG: {svg_path}")
    return svg_path


def main():
    """CLI test for image generator."""
    import sys
    
    # Test with sample data
    test_repo = {
        'repo': 'flask',
        'description': 'The Python micro framework for building web applications',
        'language': 'Python',
        'stars': 65000
    }
    
    print("Generating test cover image...")
    result = generate_cover_image(test_repo, ".")
    
    if result:
        print(f"✓ Generated: {result}")
    else:
        print("✗ Generation failed")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
