$ErrorActionPreference = "Stop"
New-Item -ItemType Directory -Force -Path "screenshots" | Out-Null
@'
from PIL import Image, ImageDraw, ImageFont
W,H=1280,720
bg=(5,8,18); panel=(13,23,39); text=(244,241,234); muted=(168,179,199); cyan=(37,215,239); green=(88,240,179); pink=(255,114,182); violet=(157,140,255)
try:
    title=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 58)
    body=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 25)
    small=ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 18)
    serif=ImageFont.truetype('C:/Windows/Fonts/georgiab.ttf', 46)
except Exception:
    title=body=small=serif=ImageFont.load_default()
im=Image.new('RGB',(W,H),bg); d=ImageDraw.Draw(im)
d.rounded_rectangle([48,48,1232,672], radius=28, fill=panel, outline=cyan, width=2)
d.text((96,106),'SNOWFLAKE CREDIT BURN VARIANCE LEDGER',font=small,fill=green)
d.text((96,178),'Credit burn variance becomes visible',font=serif,fill=text)
d.text((96,238),'before warehouse spend becomes board noise.',font=serif,fill=text)
d.text((96,332),'Warehouse credits, query waste, idle time, labels, and suspend gaps',font=body,fill=muted)
d.text((96,372),'resolve into one data-platform cost posture.',font=body,fill=muted)
for i,(label,val) in enumerate([('AGGREGATE VARIANCE','60.3'),('ESCALATION LANES','1'),('EXCESS CREDITS','1,290'),('TOP LANE','BI warehouse')]):
    x=96+i*272
    d.rounded_rectangle([x,490,x+240,604],radius=18,fill=(16,28,48),outline=(40,48,66),width=1)
    d.text((x+20,528),label,font=small,fill=muted)
    d.text((x+20,562),val,font=title if i < 3 else small,fill=text)
im.save('screenshots/01-overview-proof.png')

def card(draw, xy, size, outline, label, heading, lines, metric):
    x,y=xy; w,h=size
    draw.rounded_rectangle([x,y,x+w,y+h], radius=22, fill=panel, outline=outline, width=2)
    draw.text((x+28,y+34), label, font=small, fill=cyan)
    yy=y+82
    for line in heading:
        draw.text((x+28, yy), line, font=body, fill=text)
        yy += 34
    yy += 18
    for line in lines:
        draw.text((x+28, yy), line, font=body, fill=muted)
        yy += 31
    draw.text((x+28, y+h-86), metric, font=title, fill=text)
im=Image.new('RGB',(W,H),bg); d=ImageDraw.Draw(im)
d.text((64,70),'Snowflake burn lanes',font=serif,fill=text)
card(d,(64,150),(360,430),pink,'ESCALATE',['BI executive','warehouse'],['Idle BI windows','and missing labels','need ownership.'],'100.0')
card(d,(464,150),(360,430),violet,'WATCH',['ELT transform','warehouse'],['Transform windows','and dbt labels need','cost hygiene.'],'57.9')
card(d,(864,150),(360,430),green,'CONTAINED',['sandbox','exploration'],['Sandbox controls','remain usable for','monthly review.'],'23.0')
im.save('screenshots/02-ledger-proof.png')
'@ | python -
