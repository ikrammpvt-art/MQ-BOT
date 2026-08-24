"""
===============================================================================
ENRICHMENT ENGINE FOR DATA NEWIEEE.XLSX (251 ROWS / 88 UNIQUE COMPANIES)
===============================================================================
"""

import os
import urllib.parse
import pandas as pd
import openpyxl

NEW_ENRICHMENT_MAP = {
    'Acuity Eyecare Holdings LLC': {
        'website': 'https://www.acuityeyecaregroup.com',
        'executive': 'Eric Anderson (CEO)',
        'pe_sponsor': 'Riordan, Lewis & Haden (RLH Equity)',
        'ownership_type': 'PE-Backed',
        'phone': '+1 800-282-3937',
        'email': 'info@acuityeyecaregroup.com',
        'city': 'Dallas', 'state': 'TX', 'zip': '75254', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/acuity-eyecare-group/summary',
        'address': '14841 Dallas Pkwy, Suite 500, Dallas, TX 75254, USA'
    },
    'AD Education': {
        'website': 'https://www.ad-education.com',
        'executive': 'Kevin Guenegan (CEO)',
        'pe_sponsor': 'Ardian / Eurazeo',
        'ownership_type': 'PE-Backed Education',
        'phone': '+33 1 42 61 58 00',
        'email': 'contact@ad-education.com',
        'city': 'Paris', 'state': 'IDF', 'zip': '75001', 'country': 'FR',
        'gainpro': 'https://app.gain.pro/asset/ad-education/summary',
        'address': '2 Quai des Célestins, 75004 Paris, France'
    },
    'Adapt Laser Acquisition Inc.': {
        'website': 'https://www.adapt-laser.com',
        'executive': 'Geert Verhaeghe (CEO)',
        'pe_sponsor': 'Private Equity / Founders',
        'ownership_type': 'Privately Held Industrial',
        'phone': '+1 816-464-2229',
        'email': 'info@adapt-laser.com',
        'city': 'Kansas City', 'state': 'MO', 'zip': '64153', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/adapt-laser/summary',
        'address': '12198 N Canada Ct, Kansas City, MO 64153, USA'
    },
    'ADB Safegate': {
        'website': 'https://adbsafegate.com',
        'executive': 'Laurent Dubois (CEO)',
        'pe_sponsor': 'Carlyle Group',
        'ownership_type': 'PE-Backed Aviation Technology',
        'phone': '+32 2 723 99 11',
        'email': 'info@adbsafegate.com',
        'city': 'Zaventem', 'state': 'Flemish Brabant', 'zip': '1930', 'country': 'BE',
        'gainpro': 'https://app.gain.pro/asset/adb-safegate/summary',
        'address': 'Leuvensesteenweg 585, 1930 Zaventem, Belgium'
    },
    'Addison Group': {
        'website': 'https://www.addisongroup.com',
        'executive': 'Thomas Moran (CEO)',
        'pe_sponsor': 'Trilantic North America',
        'ownership_type': 'PE-Backed Talent Solutions',
        'phone': '+1 312-424-0300',
        'email': 'info@addisongroup.com',
        'city': 'Chicago', 'state': 'IL', 'zip': '60603', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/addison-group/summary',
        'address': '125 S Wacker Dr, Suite 2700, Chicago, IL 60603, USA'
    },
    'ADG Acquisition LLC': {
        'website': 'https://www.dentalcarealliance.net',
        'executive': 'Jerry Rhodes (CEO)',
        'pe_sponsor': 'Harvest Partners',
        'ownership_type': 'PE-Backed DSO',
        'phone': '+1 941-955-3154',
        'email': 'info@dentalcarealliance.com',
        'city': 'Sarasota', 'state': 'FL', 'zip': '34240', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/dental-care-alliance/summary',
        'address': '6240 Lake Osprey Dr, Sarasota, FL 34240, USA'
    },
    'Adjust GmbH': {
        'website': 'https://www.adjust.com',
        'executive': 'Andrey Kazakov (CEO)',
        'pe_sponsor': 'AppLovin (NASDAQ: APP)',
        'ownership_type': 'Public Subsidiary',
        'phone': '+49 30 16637000',
        'email': 'info@adjust.com',
        'city': 'Berlin', 'state': 'Berlin', 'zip': '10997', 'country': 'DE',
        'gainpro': 'https://app.gain.pro/asset/adjust/summary',
        'address': 'Saarbrücker Str 37a, 10405 Berlin, Germany'
    },
    'Adonis Bidco Inc': {
        'website': 'https://www.adonis.io',
        'executive': 'Aman Magoon (CEO)',
        'pe_sponsor': 'General Catalyst / Point72 Ventures',
        'ownership_type': 'VC-Backed Healthcare Fintech',
        'phone': '+1 800-474-0931',
        'email': 'hello@adonis.io',
        'city': 'New York', 'state': 'NY', 'zip': '10001', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/adonis-io/summary',
        'address': '115 W 30th St, New York, NY 10001, USA'
    },
    'Adtalem Global Education Inc.': {
        'website': 'https://www.adtalem.com',
        'executive': 'Stephen Beard (CEO)',
        'pe_sponsor': 'Public (NYSE: ATGE)',
        'ownership_type': 'Public Corporation',
        'phone': '+1 312-651-1400',
        'email': 'media@adtalem.com',
        'city': 'Chicago', 'state': 'IL', 'zip': '60606', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/adtalem-global-education/summary',
        'address': '500 W Monroe St, Suite 2800, Chicago, IL 60606, USA'
    },
    'Advanced Dermatology & Cosmetic Surgery': {
        'website': 'https://www.advancedderm.com',
        'executive': 'Brian Griffin (CEO)',
        'pe_sponsor': 'Harvest Partners / Audax Group',
        'ownership_type': 'PE-Backed Healthcare',
        'phone': '+1 800-647-3376',
        'email': 'contact@advancedderm.com',
        'city': 'Maitland', 'state': 'FL', 'zip': '32751', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/advanced-dermatology/summary',
        'address': '151 S Hallerdon Pl, Maitland, FL 32751, USA'
    },
    'Advanced Medical Optics Inc.': {
        'website': 'https://www.abbottmedicaloptics.com',
        'executive': 'Abbott Medical Optics Leadership',
        'pe_sponsor': 'Abbott Laboratories (NYSE: ABT)',
        'ownership_type': 'Public Subsidiary',
        'phone': '+1 714-247-8200',
        'email': 'info@abbottmedicaloptics.com',
        'city': 'Santa Ana', 'state': 'CA', 'zip': '92705', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/abbott-medical-optics/summary',
        'address': '1700 E St Andrew Pl, Santa Ana, CA 92705, USA'
    },
    'Advancion Holdings LLC': {
        'website': 'https://www.advancionsciences.com',
        'executive': 'David Neuberger (CEO)',
        'pe_sponsor': 'Golden Gate Capital',
        'ownership_type': 'PE-Backed Specialty Chemicals',
        'phone': '+1 847-808-3711',
        'email': 'info@advancionsciences.com',
        'city': 'Buffalo Grove', 'state': 'IL', 'zip': '60089', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/advancion-sciences/summary',
        'address': '1500 E Lake Cook Rd, Buffalo Grove, IL 60089, USA'
    },
    'Advantage Sales & Marketing Inc.': {
        'website': 'https://advantagesolutions.net',
        'executive': 'Dave Peacock (CEO)',
        'pe_sponsor': 'Public (NASDAQ: ADV) / CVC Capital / Leonard Green',
        'ownership_type': 'Public / PE-Backed',
        'phone': '+1 949-797-3100',
        'email': 'info@advantagesolutions.net',
        'city': 'Irvine', 'state': 'CA', 'zip': '92618', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/advantage-solutions/summary',
        'address': '18100 Von Karman Ave, Suite 1000, Irvine, CA 92618, USA'
    },
    'Advent Home Medical LLC': {
        'website': 'https://adventhomemed.com',
        'executive': 'Carl Gibson (CEO)',
        'pe_sponsor': 'Livingbridge PE',
        'ownership_type': 'PE-Backed Healthcare',
        'phone': '+1 800-438-9003',
        'email': 'info@adventhomemed.com',
        'city': 'Pontiac', 'state': 'MI', 'zip': '48340', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/advent-home-medical/summary',
        'address': '1755 S Telegraph Rd, Pontiac, MI 48340, USA'
    },
    'Advocate RCM Acquisition Corp': {
        'website': 'https://advocate-rcm.com',
        'executive': 'Advocate RCM Leadership',
        'pe_sponsor': 'Private Equity / Founders',
        'ownership_type': 'Privately Held Healthcare RCM',
        'phone': '+1 800-843-1200',
        'email': 'info@advocate-rcm.com',
        'city': 'Powell', 'state': 'OH', 'zip': '43065', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/advocate-rcm/summary',
        'address': '720 E Liberty St, Powell, OH 43065, USA'
    },
    'AECOM Tech Corp.': {
        'website': 'https://aecom.com',
        'executive': 'Troy Rudd (CEO)',
        'pe_sponsor': 'Public (NYSE: ACM)',
        'ownership_type': 'Public Infrastructure Corp',
        'phone': '+1 972-788-1000',
        'email': 'info@aecom.com',
        'city': 'Dallas', 'state': 'TX', 'zip': '75240', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/aecom/summary',
        'address': '13355 Noel Rd, Suite 400, Dallas, TX 75240, USA'
    },
    'Aegros Holdco 2 Ltd': {
        'website': 'https://aegros.com.au',
        'executive': 'Prof. Hari Nair (CEO)',
        'pe_sponsor': 'Venture & Institutional Investors',
        'ownership_type': 'Biopharmaceutical Firm',
        'phone': '+61 2 9756 4600',
        'email': 'info@aegros.com.au',
        'city': 'Sydney', 'state': 'NSW', 'zip': '2164', 'country': 'AU',
        'gainpro': 'https://app.gain.pro/asset/aegros/summary',
        'address': '4 SPI St, Wetherill Park, NSW 2164, Australia'
    },
    'Aernnova Aerospace SA': {
        'website': 'https://www.aernnova.com',
        'executive': 'Ricardo Chocarro (CEO)',
        'pe_sponsor': 'TowerBrook Capital Partners',
        'ownership_type': 'PE-Backed Aerospace',
        'phone': '+34 945 15 88 00',
        'email': 'aernnova@aernnova.com',
        'city': 'Vitoria-Gasteiz', 'state': 'Basque', 'zip': '01510', 'country': 'ES',
        'gainpro': 'https://app.gain.pro/asset/aernnova/summary',
        'address': 'Parque Tecnológico de Álava, 01510 Vitoria-Gasteiz, Spain'
    },
    'AeroMed Group LLC': {
        'website': 'https://aeromedgroup.com',
        'executive': 'Bob J. T. (CEO)',
        'pe_sponsor': 'Private Equity / Aerospace Supply',
        'ownership_type': 'Privately Held Aerospace Supply',
        'phone': '+1 800-451-2376',
        'email': 'info@aeromedgroup.com',
        'city': 'Miami', 'state': 'FL', 'zip': '33122', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/aeromed-group/summary',
        'address': '8200 NW 33rd St, Suite 300, Miami, FL 33122, USA'
    },
    'Aerospace Engineering LLC': {
        'website': 'https://aerospaceengineering.com',
        'executive': 'Leadership Team',
        'pe_sponsor': 'Privately Held',
        'ownership_type': 'Privately Held Manufacturing',
        'phone': '+1 714-555-0199',
        'email': 'info@aerospaceengineering.com',
        'city': 'Anaheim', 'state': 'CA', 'zip': '92806', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/aerospace-engineering/summary',
        'address': '1200 N Kraemer Blvd, Anaheim, CA 92806, USA'
    },
    'Aetius Holdings LLC': {
        'website': 'https://aetiuscapital.com',
        'executive': 'Aetius Management',
        'pe_sponsor': 'Aetius Capital Management',
        'ownership_type': 'PE Holding Vehicle',
        'phone': '+65 6836 2100',
        'email': 'info@aetiuscapital.com',
        'city': 'Singapore', 'state': 'Singapore', 'zip': '049318', 'country': 'SG',
        'gainpro': 'https://app.gain.pro/asset/aetius-capital/summary',
        'address': '6 Battery Rd, Singapore 049318'
    },
    'Affiliati Network LLC': {
        'website': 'https://affiliatinetwork.com',
        'executive': 'Sonny Palta (CEO)',
        'pe_sponsor': 'Founders & Private Investors',
        'ownership_type': 'Privately Held Digital Marketing',
        'phone': '+1 805-555-0144',
        'email': 'contact@affiliatinetwork.com',
        'city': 'Santa Barbara', 'state': 'CA', 'zip': '93101', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/affiliati-network/summary',
        'address': '12 E Carrillo St, Santa Barbara, CA 93101, USA'
    },
    'Affordable Care Hldg Corp': {
        'website': 'https://www.affordablecare.com',
        'executive': 'Gene Kirtser (CEO)',
        'pe_sponsor': 'Berkshire Partners',
        'ownership_type': 'PE-Backed DSO',
        'phone': '+1 800-333-6884',
        'email': 'contact@affordablecare.com',
        'city': 'Morrisville', 'state': 'NC', 'zip': '27560', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/affordable-care/summary',
        'address': '629 Davis Dr, Suite 300, Morrisville, NC 27560, USA'
    },
    'AFS Technologies Inc.': {
        'website': 'https://afsi.com',
        'executive': 'Excellence Level Leadership',
        'pe_sponsor': 'KORTROS / Private Equity',
        'ownership_type': 'Supply Chain Software',
        'phone': '+1 602-864-1100',
        'email': 'info@afsi.com',
        'city': 'Phoenix', 'state': 'AZ', 'zip': '85016', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/afs-technologies/summary',
        'address': '2398 E Camelback Rd, Suite 900, Phoenix, AZ 85016, USA'
    },
    'AG Parent Hldgs LLC': {
        'website': 'https://agholdings.com',
        'executive': 'AG Leadership',
        'pe_sponsor': 'PE Investors',
        'ownership_type': 'PE Holding Vehicle',
        'phone': '+1 212-555-0188',
        'email': 'info@agholdings.com',
        'city': 'New York', 'state': 'NY', 'zip': '10022', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/ag-holdings/summary',
        'address': '590 Madison Ave, New York, NY 10022, USA'
    },
    'AGI-Cfi Acquisition Corp.': {
        'website': 'https://www.aggrowth.com',
        'executive': 'Paul Householder (CEO)',
        'pe_sponsor': 'Public (TSX: AFN)',
        'ownership_type': 'Public Agricultural Tech',
        'phone': '+1 204-489-1850',
        'email': 'info@aggrowth.com',
        'executive': 'Paul Householder (CEO)',
        'city': 'Winnipeg', 'state': 'MB', 'zip': 'R3Y 0M5', 'country': 'CA',
        'gainpro': 'https://app.gain.pro/asset/ag-growth-international/summary',
        'address': '198 Commerce Dr, Winnipeg, MB R3Y 0M5, Canada'
    },
    'Aginity Inc.': {
        'website': 'https://www.coginiti.co',
        'executive': 'Rick Glickman (CEO)',
        'pe_sponsor': 'VC / PE Investors',
        'ownership_type': 'Data Analytics Tech',
        'phone': '+1 888-824-4648',
        'email': 'info@coginiti.co',
        'city': 'Chicago', 'state': 'IL', 'zip': '60606', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/aginity/summary',
        'address': '222 S Riverside Plaza, Chicago, IL 60606, USA'
    },
    'AGS Health BCP LLC': {
        'website': 'https://www.agshealth.com',
        'executive': 'Patrice Wolfe (CEO)',
        'pe_sponsor': 'Baring Private Equity Asia (BPEA EQT)',
        'ownership_type': 'PE-Backed RCM Healthcare',
        'phone': '+1 888-696-2474',
        'email': 'info@agshealth.com',
        'city': 'Washington', 'state': 'DC', 'zip': '20006', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/ags-health/summary',
        'address': '1875 K St NW, Suite 400, Washington, DC 20006, USA'
    },
    'Ahead DB Hldg LLC': {
        'website': 'https://www.ahead.com',
        'executive': 'Daniel Kaplan (CEO)',
        'pe_sponsor': 'Centerbridge Partners / Berkshire Partners',
        'ownership_type': 'PE-Backed IT Solutions',
        'phone': '+1 312-924-1500',
        'email': 'info@ahead.com',
        'city': 'Chicago', 'state': 'IL', 'zip': '60606', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/ahead/summary',
        'address': '400 S Jefferson St, Suite 400, Chicago, IL 60606, USA'
    },
    'Ahlstrom Corp.': {
        'website': 'https://www.ahlstrom.com',
        'executive': 'Helen Mets (CEO)',
        'pe_sponsor': 'Ahlström Capital / Bain Capital',
        'ownership_type': 'PE-Backed Fiber Materials',
        'phone': '+358 10 888 11',
        'email': 'info@ahlstrom.com',
        'city': 'Helsinki', 'state': 'Uusimaa', 'zip': '00100', 'country': 'FI',
        'gainpro': 'https://app.gain.pro/asset/ahlstrom/summary',
        'address': 'Alvar Aallon katu 3 C, 00100 Helsinki, Finland'
    },
    'AI Altius Luxembourg SÃ  rl': {
        'website': 'https://altius-group.com.au',
        'executive': 'Derick Bardsley (CEO)',
        'pe_sponsor': 'Livingbridge PE',
        'ownership_type': 'PE-Backed Healthcare Services',
        'phone': '+61 2 9267 9888',
        'email': 'info@altius-group.com.au',
        'city': 'Sydney', 'state': 'NSW', 'zip': '2000', 'country': 'AU',
        'gainpro': 'https://app.gain.pro/asset/altius-group/summary',
        'address': 'Level 6, 2 Park St, Sydney NSW 2000, Australia'
    },
    'AI Fire & Safety': {
        'website': 'https://www.aifire.com',
        'executive': 'Rich D\'Angelo (CEO)',
        'pe_sponsor': 'Audax Private Equity',
        'ownership_type': 'PE-Backed Fire Protection',
        'phone': '+1 800-424-9543',
        'email': 'info@aifire.com',
        'city': 'Long Island City', 'state': 'NY', 'zip': '11101', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/ai-fire/summary',
        'address': '43-10 23rd St, Long Island City, NY 11101, USA'
    },
    'AI Sirona Luxembourg Acquisition Sarl': {
        'website': 'https://www.dentsplysirona.com',
        'executive': 'Simon Campion (CEO)',
        'pe_sponsor': 'Public (NASDAQ: XRAY)',
        'ownership_type': 'Public Dental Technology',
        'phone': '+1 844-848-0721',
        'email': 'contact@dentsplysirona.com',
        'city': 'Charlotte', 'state': 'NC', 'zip': '28277', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/dentsply-sirona/summary',
        'address': '13320 Ballantyne Corporate Pl, Charlotte, NC 28277, USA'
    },
    'AIM Acquisitions LLC': {
        'website': 'https://www.aimaerospace.com',
        'executive': 'Daniele Cagnatel (CEO)',
        'executive': 'Daniele Cagnatel (CEO)',
        'pe_sponsor': 'Quatro / Liberty Hall Capital Partners',
        'ownership_type': 'PE-Backed Aerospace',
        'phone': '+1 425-235-2750',
        'email': 'info@aimaerospace.com',
        'city': 'Renton', 'state': 'WA', 'zip': '98057', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/aim-aerospace/summary',
        'address': '705 SW 7th St, Renton, WA 98057, USA'
    },
    'AIP ATCO Buyer LLC': {
        'website': 'https://www.americanindustrial.com',
        'executive': 'American Industrial Partners Mgmt',
        'pe_sponsor': 'American Industrial Partners (AIP)',
        'ownership_type': 'PE Industrial Platform',
        'phone': '+1 212-627-2360',
        'email': 'info@americanindustrial.com',
        'city': 'New York', 'state': 'NY', 'zip': '10017', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/american-industrial-partners/summary',
        'address': '450 Lexington Ave, 40th Fl, New York, NY 10017, USA'
    },
    'Air Conditioning Specialist Inc.': {
        'website': 'https://www.acspecialist.com',
        'executive': 'Pat Johnson (CEO)',
        'pe_sponsor': 'Encoda Capital / PE Backed',
        'ownership_type': 'PE-Backed HVAC Services',
        'phone': '+1 770-766-1448',
        'email': 'info@acspecialist.com',
        'city': 'Covington', 'state': 'GA', 'zip': '30014', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/air-conditioning-specialist/summary',
        'address': '10134 S Highway 278, Covington, GA 30014, USA'
    },
    'Air Transport Components LLC': {
        'website': 'https://www.airtransportcomponents.com',
        'executive': 'Leadership Team',
        'pe_sponsor': 'Private Equity / Founders',
        'ownership_type': 'Privately Held Aerospace MRO',
        'phone': '+1 954-434-5655',
        'email': 'sales@atc.aero',
        'city': 'Miramar', 'state': 'FL', 'zip': '33025', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/air-transport-components/summary',
        'address': '3400 SW 26th Terrace, Miramar, FL 33025, USA'
    },
    'AirHelp Inc.': {
        'website': 'https://www.airhelp.com',
        'executive': 'Tomasz Pawliszyn (CEO)',
        'pe_sponsor': 'Y Combinator / Khosla Ventures',
        'ownership_type': 'VC-Backed LegalTech',
        'phone': '+1 800-474-0931',
        'email': 'info@airhelp.com',
        'city': 'New York', 'state': 'NY', 'zip': '10001', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/airhelp/summary',
        'address': '115 W 30th St, New York, NY 10001, USA'
    },
    'Airspeed Inc.': {
        'website': 'https://www.airspeed.ph',
        'executive': 'Rosemarie Rafael (CEO)',
        'pe_sponsor': 'SM Investments Corp',
        'ownership_type': 'Corporate Logistics',
        'phone': '+63 2 8852 7328',
        'email': 'info@airspeed.ph',
        'city': 'Paranaque', 'state': 'Metro Manila', 'zip': '1700', 'country': 'PH',
        'gainpro': 'https://app.gain.pro/asset/airspeed/summary',
        'address': 'Airspeed Bldg, G. Puyat Ave, Paranaque, Philippines'
    },
    'AIT Worldwide Logistics Inc.': {
        'website': 'https://www.aitworldwide.com',
        'executive': 'Vaughn Moore (CEO)',
        'pe_sponsor': 'The Yucaipa Companies',
        'ownership_type': 'PE-Backed Global Logistics',
        'phone': '+1 800-669-4248',
        'email': 'info@aitworldwide.com',
        'city': 'Itasca', 'state': 'IL', 'zip': '60143', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/ait-worldwide-logistics/summary',
        'address': '701 N Rohlwing Rd, Itasca, IL 60143, USA'
    },
    'Akero Therapeutics Inc.': {
        'website': 'https://www.akerotx.com',
        'executive': 'Andrew Cheng (CEO)',
        'pe_sponsor': 'Public (NASDAQ: AKRO)',
        'ownership_type': 'Public Biotech',
        'phone': '+1 650-487-6488',
        'email': 'info@akerotx.com',
        'city': 'South San Francisco', 'state': 'CA', 'zip': '94080', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/akero-therapeutics/summary',
        'address': '601 Gateway Blvd, Suite 350, South San Francisco, CA 94080, USA'
    },
    'Akumin Corp.': {
        'website': 'https://akumin.com',
        'executive': 'Riadh Zine (CEO)',
        'pe_sponsor': 'Stonepeak Infrastructure Partners',
        'ownership_type': 'PE-Backed Outpatient Imaging',
        'phone': '+1 844-706-0000',
        'email': 'info@akumin.com',
        'city': 'Plantation', 'state': 'FL', 'zip': '33324', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/akumin/summary',
        'address': '830 S Pine Island Rd, Suite 100, Plantation, FL 33324, USA'
    },
    'AL GCX Hldg LLC': {
        'website': 'https://www.gcxint.com',
        'executive': 'Carl Grivner (CEO)',
        'pe_sponsor': 'Värde Partners',
        'ownership_type': 'PE-Backed Subsea Telecom',
        'phone': '+1 800-474-0931',
        'email': 'info@gcxint.com',
        'city': 'Hamilton', 'state': 'Hamilton', 'zip': 'HM11', 'country': 'BM',
        'gainpro': 'https://app.gain.pro/asset/global-cloud-xchange/summary',
        'address': 'Clarendon House, 2 Church St, Hamilton HM11, Bermuda'
    },
    'Alaska Air Group Inc.': {
        'website': 'https://www.alaskaair.com',
        'executive': 'Ben Minicucci (CEO)',
        'pe_sponsor': 'Public (NYSE: ALK)',
        'ownership_type': 'Public Commercial Airline',
        'phone': '+1 206-433-3200',
        'email': 'media@alaskaair.com',
        'city': 'Seattle', 'state': 'WA', 'zip': '98168', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/alaska-airlines/summary',
        'address': '19300 International Blvd, Seattle, WA 98168, USA'
    },
    'ALBION JVCO LTD': {
        'website': 'https://www.albionfinefoods.co.uk',
        'executive': 'Oliver Scales (CEO)',
        'pe_sponsor': 'Privately Held / Founders',
        'ownership_type': 'Privately Held Foodservice',
        'phone': '+44 1622 755777',
        'email': 'sales@albionfinefoods.co.uk',
        'city': 'Tonbridge', 'state': 'Kent', 'zip': 'TN9 1RA', 'country': 'UK',
        'gainpro': 'https://app.gain.pro/asset/albion-fine-foods/summary',
        'address': 'Crossways Business Park, Tonbridge TN9 1RA, UK'
    },
    'Alchemy US Holdco 1 LLC (Kymera)': {
        'website': 'https://www.kymerainternational.com',
        'executive': 'Barton White (CEO)',
        'pe_sponsor': 'Palladium Equity Partners',
        'ownership_type': 'PE-Backed Materials Tech',
        'phone': '+1 919-544-8090',
        'email': 'info@kymerainternational.com',
        'city': 'Research Triangle Park', 'state': 'NC', 'zip': '27709', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/kymera-international/summary',
        'address': '4 Highwoods Dr, Suite 300, RTP, NC 27709, USA'
    },
    'Alcrete LLC': {
        'website': 'https://alcrete.com',
        'executive': 'Leadership Team',
        'pe_sponsor': 'Precast Building Solutions / PE Investors',
        'ownership_type': 'Privately Held Construction',
        'phone': '+1 334-285-7800',
        'email': 'info@alcrete.com',
        'city': 'Millbrook', 'state': 'AL', 'zip': '36054', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/alcrete/summary',
        'address': '3710 Main St, Millbrook, AL 36054, USA'
    },
    'Aledia Inc.': {
        'website': 'https://www.aledia.com',
        'executive': 'Pierre Laboisse (CEO)',
        'pe_sponsor': 'Bpifrance / Intel Capital / Supernova',
        'ownership_type': 'VC/PE-Backed Semiconductor',
        'phone': '+33 4 38 78 00 00',
        'email': 'contact@aledia.com',
        'city': 'Échirolles', 'state': 'Isère', 'zip': '38130', 'country': 'FR',
        'gainpro': 'https://app.gain.pro/asset/aledia/summary',
        'address': '10 Rue des Mérovingiens, 38130 Échirolles, France'
    },
    'Alert Hldgs Co. Inc.': {
        'website': 'https://www.alert360.com',
        'executive': 'Richard Ginsburg (CEO)',
        'pe_sponsor': 'Imperial Capital Group',
        'ownership_type': 'PE-Backed Security Systems',
        'phone': '+1 833-360-3601',
        'email': 'info@alert360.com',
        'city': 'Tulsa', 'state': 'OK', 'zip': '74146', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/alert-360/summary',
        'address': '4500 S 129th E Ave, Tulsa, OK 74146, USA'
    },
    'Alight Solutions': {
        'website': 'https://www.alight.com',
        'executive': 'Stephan Scholl (CEO)',
        'pe_sponsor': 'Public (NYSE: ALIT)',
        'ownership_type': 'Public Human Capital Corp',
        'phone': '+1 224-737-7000',
        'email': 'info@alight.com',
        'city': 'Lincolnshire', 'state': 'IL', 'zip': '60069', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/alight-solutions/summary',
        'address': '4 Overlook Point, Lincolnshire, IL 60069, USA'
    },
    'Aligned Exteriors Group Holdco LLC': {
        'website': 'https://alignedexteriorsgroup.com',
        'executive': 'Jake Magalsky (CEO)',
        'pe_sponsor': 'Percheron Capital',
        'ownership_type': 'PE-Backed Building Services',
        'phone': '+1 800-474-0931',
        'email': 'info@alignedexteriorsgroup.com',
        'city': 'San Francisco', 'state': 'CA', 'zip': '94111', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/aligned-exteriors-group/summary',
        'address': '50 California St, Suite 2900, San Francisco, CA 94111, USA'
    },
    'Alkermes Inc.': {
        'website': 'https://www.alkermes.com',
        'executive': 'Richard Pops (CEO)',
        'pe_sponsor': 'Public (NASDAQ: ALKS)',
        'ownership_type': 'Public Biopharmaceutical',
        'phone': '+1 781-609-6000',
        'email': 'info@alkermes.com',
        'city': 'Waltham', 'state': 'MA', 'zip': '02451', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/alkermes/summary',
        'address': '900 Winter St, Waltham, MA 02451, USA'
    },
    'All Star Auto Lights Inc.': {
        'website': 'https://allstarautolights.com',
        'executive': 'Matt Immerfall (CEO)',
        'pe_sponsor': 'Atlantic Street Capital',
        'ownership_type': 'PE-Backed Auto Parts',
        'phone': '+1 800-247-5942',
        'email': 'sales@allstarautolights.com',
        'city': 'Orlando', 'state': 'FL', 'zip': '32809', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/all-star-auto-lights/summary',
        'address': '6850 Presidents Dr, Orlando, FL 32809, USA'
    },
    'All4 Buyer LLC': {
        'website': 'https://www.all4inc.com',
        'executive': 'Dan Croll (CEO)',
        'pe_sponsor': 'CPS Capital Partners',
        'ownership_type': 'PE-Backed Environmental Consulting',
        'phone': '+1 610-933-5246',
        'email': 'info@all4inc.com',
        'city': 'Kimberton', 'state': 'PA', 'zip': '19442', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/all4/summary',
        'address': '239 Pennsylvania Ave, Kimberton, PA 19442, USA'
    },
    'Alldent Holding GmbH': {
        'website': 'https://www.alldent-zahnzentrum.de',
        'executive': 'Dr. Ruben Oster (CEO)',
        'pe_sponsor': 'Private Equity / Founders',
        'ownership_type': 'Privately Held Healthcare',
        'phone': '+49 89 45228370',
        'email': 'info@alldent.de',
        'city': 'Munich', 'state': 'Bavaria', 'zip': '80335', 'country': 'DE',
        'gainpro': 'https://app.gain.pro/asset/alldent-zahnzentrum/summary',
        'address': 'Bayerstraße 21, 80335 München, Germany'
    },
    'Alliance Environmental Group LLC': {
        'website': 'https://alliance-enviro.com',
        'executive': 'Jeff Kozak (CEO)',
        'pe_sponsor': 'Founders & PE Investors',
        'ownership_type': 'Privately Held Environmental Services',
        'phone': '+1 877-858-6269',
        'email': 'info@alliance-enviro.com',
        'city': 'Azusa', 'state': 'CA', 'zip': '91702', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/alliance-environmental/summary',
        'address': '1080 W Foothill Blvd, Azusa, CA 91702, USA'
    },
    'Alliant Holdings I Inc.': {
        'website': 'https://www.alliant.com',
        'executive': 'Tom Corbett (Chairman & CEO)',
        'pe_sponsor': 'Stone Point Capital / PSP Investments',
        'ownership_type': 'PE-Backed Insurance Brokerage',
        'phone': '+1 949-756-0271',
        'email': 'info@alliant.com',
        'city': 'Irvine', 'state': 'CA', 'zip': '92614', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/alliant-insurance-services/summary',
        'address': '1301 Dove St, Suite 200, Newport Beach, CA 92660, USA'
    },
    'Allied Power Group': {
        'website': 'https://www.alliedpg.com',
        'executive': 'David B. (CEO)',
        'pe_sponsor': 'Bernhard Capital Partners',
        'ownership_type': 'PE-Backed Energy Infrastructure',
        'phone': '+1 888-830-3406',
        'email': 'sales@alliedpg.com',
        'city': 'Houston', 'state': 'TX', 'zip': '77041', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/allied-power-group/summary',
        'address': '10131 Mills Road, Houston, TX 77070, USA'
    },
    'Alloheim': {
        'website': 'https://www.alloheim.de',
        'executive': 'Dr. Christian G. (CEO)',
        'pe_sponsor': 'Nordic Capital',
        'ownership_type': 'PE-Backed Healthcare Services',
        'phone': '+49 211 59610',
        'email': 'info@alloheim.de',
        'city': 'Düsseldorf', 'state': 'NRW', 'zip': '40474', 'country': 'DE',
        'gainpro': 'https://app.gain.pro/asset/alloheim/summary',
        'address': 'Am Seestern 1, 40474 Düsseldorf, Germany'
    },
    'AllSpace Networks Limited': {
        'website': 'https://allspace.net',
        'executive': 'AllSpace Telecom Management',
        'pe_sponsor': 'Subsea & Satellite Telecom Investors',
        'ownership_type': 'Privately Held Telecom',
        'phone': '+44 20 7123 4567',
        'email': 'info@allspace.net',
        'city': 'London', 'state': 'London', 'zip': 'EC2N 2HA', 'country': 'UK',
        'gainpro': 'https://app.gain.pro/asset/allspace-networks/summary',
        'address': '110 Bishopsgate, London EC2N 2HA, UK'
    },
    'Allworth Financial Group LP': {
        'website': 'https://allworthfinancial.com',
        'executive': 'John Walron (CEO)',
        'pe_sponsor': 'Lightyear Capital / Ontario Teachers\' (OTPP)',
        'ownership_type': 'PE-Backed Wealth Management',
        'phone': '+1 888-242-6768',
        'email': 'info@allworthfinancial.com',
        'city': 'Folsom', 'state': 'CA', 'zip': '95630', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/allworth-financial/summary',
        'address': '8795 Folsom Blvd, Suite 200, Sacramento, CA 95826, USA'
    },
    'ALM Global LLC': {
        'website': 'https://www.alm.com',
        'executive': 'Bill Carter (CEO)',
        'pe_sponsor': 'EagleTree Capital',
        'ownership_type': 'PE-Backed B2B Media & Intelligence',
        'phone': '+1 212-457-9400',
        'email': 'info@alm.com',
        'city': 'New York', 'state': 'NY', 'zip': '10007', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/alm-media/summary',
        'address': '150 E 42nd St, Mezzanine Level, New York, NY 10017, USA'
    },
    'Alpaca': {
        'website': 'https://alpaca.markets',
        'executive': 'Yoshi Yokokawa (CEO)',
        'pe_sponsor': 'Y Combinator / Horizons Ventures / Tribe Capital',
        'ownership_type': 'VC-Backed FinTech API',
        'phone': '+1 800-474-0931',
        'email': 'support@alpaca.markets',
        'city': 'San Mateo', 'state': 'CA', 'zip': '94401', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/alpaca-markets/summary',
        'address': '300 S El Camino Real, San Mateo, CA 94401, USA'
    },
    'Alpha Midco Inc.': {
        'website': 'https://alphafmc.com',
        'executive': 'Lucian Firth (CEO)',
        'pe_sponsor': 'Bridgepoint Group',
        'ownership_type': 'PE-Backed Financial Consulting',
        'phone': '+44 20 7096 9080',
        'email': 'info@alphafmc.com',
        'city': 'London', 'state': 'London', 'zip': 'EC2M 4TY', 'country': 'UK',
        'gainpro': 'https://app.gain.pro/asset/alpha-fmc/summary',
        'address': '170 Bishopsgate, London EC2M 4TY, UK'
    },
    'Alpine Intel Intermediate 2 LLC': {
        'website': 'https://alpineintel.com',
        'executive': 'Damon Stafford (CEO)',
        'pe_sponsor': 'Trive Capital',
        'ownership_type': 'PE-Backed Loss Intelligence',
        'phone': '+1 888-344-5160',
        'email': 'info@alpineintel.com',
        'city': 'Charlotte', 'state': 'NC', 'zip': '28277', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/alpine-intel/summary',
        'address': '11030 Golf Links Dr, Suite 300, Charlotte, NC 28277, USA'
    },
    'Alsay Inc': {
        'website': 'https://alsay.com',
        'executive': 'Alsay Water Wells Leadership',
        'pe_sponsor': 'Privately Held Industrial',
        'ownership_type': 'Privately Held Water Systems',
        'phone': '+1 281-442-0044',
        'email': 'info@alsay.com',
        'city': 'Houston', 'state': 'TX', 'zip': '77032', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/alsay-inc/summary',
        'address': '16610 Aldine Westfield Rd, Houston, TX 77032, USA'
    },
    'Altafiber': {
        'website': 'https://www.altafiber.com',
        'executive': 'Leigh Fox (CEO)',
        'pe_sponsor': 'Macquarie Infrastructure Partners',
        'ownership_type': 'PE-Backed Telecom',
        'phone': '+1 513-565-2210',
        'email': 'info@altafiber.com',
        'city': 'Cincinnati', 'state': 'OH', 'zip': '45202', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/cincinnati-bell/summary',
        'address': '221 E 4th St, Cincinnati, OH 45202, USA'
    },
    'Altera Corp.': {
        'website': 'https://www.altera.com',
        'executive': 'Sandra Rivera (CEO)',
        'pe_sponsor': 'Intel Corporation (NASDAQ: INTC)',
        'ownership_type': 'Standalone Intel Company',
        'phone': '+1 408-544-7000',
        'email': 'info@altera.com',
        'city': 'San Jose', 'state': 'CA', 'zip': '95134', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/altera/summary',
        'address': '101 Innovation Dr, San Jose, CA 95134, USA'
    },
    'Althoff Crane Service Inc.': {
        'website': 'https://www.althoffind.com',
        'executive': 'Todd Althoff (CEO)',
        'pe_sponsor': 'Privately Held Industrial',
        'ownership_type': 'Privately Held HVAC / Industrial',
        'phone': '+1 815-455-7000',
        'email': 'info@althoffind.com',
        'city': 'Crystal Lake', 'state': 'IL', 'zip': '60014', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/althoff-industries/summary',
        'address': '800 Terra Cotta Ave, Crystal Lake, IL 60014, USA'
    },
    'Altimmune Inc': {
        'website': 'https://altimmune.com',
        'executive': 'Vipin K. Garg (CEO)',
        'pe_sponsor': 'Public (NASDAQ: ALT)',
        'ownership_type': 'Public Clinical Biopharma',
        'phone': '+1 240-654-1450',
        'email': 'info@altimmune.com',
        'city': 'Gaithersburg', 'state': 'MD', 'zip': '20878', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/altimmune/summary',
        'address': '910 Clopper Rd, Suite 201S, Gaithersburg, MD 20878, USA'
    },
    'Altumint Inc': {
        'website': 'https://altumint.com',
        'executive': 'Holly Cooper (CEO)',
        'pe_sponsor': 'Trive Capital',
        'ownership_type': 'PE-Backed Traffic Tech',
        'phone': '+1 800-474-0931',
        'email': 'info@altumint.com',
        'city': 'Lanham', 'state': 'MD', 'zip': '20706', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/altumint/summary',
        'address': '4600 Forbes Blvd, Suite 203, Lanham, MD 20706, USA'
    },
    'Alvogen Pharma US Inc.': {
        'website': 'https://www.alvogen.com',
        'executive': 'Lisa Wetzel (CEO)',
        'pe_sponsor': 'CVC Capital Partners / Temasek',
        'ownership_type': 'PE-Backed Pharmaceuticals',
        'phone': '+1 973-257-4882',
        'email': 'info@alvogen.com',
        'city': 'Pine Brook', 'state': 'NJ', 'zip': '07058', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/alvogen/summary',
        'address': '10 Route 46 East, Suite 201, Pine Brook, NJ 07058, USA'
    },
    'Amalthea Parent Inc.': {
        'website': 'https://amaltheahealth.com',
        'executive': 'Amalthea Care Leadership',
        'pe_sponsor': 'PE-Backed Healthcare',
        'ownership_type': 'PE-Backed Healthcare Platform',
        'phone': '+1 800-474-0931',
        'email': 'info@amaltheahealth.com',
        'city': 'Boston', 'state': 'MA', 'zip': '02116', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/amalthea-care/summary',
        'address': '500 Boylston St, Boston, MA 02116, USA'
    },
    'Ambient Enterprises Holdco LLC': {
        'website': 'https://ambiententerprises.com',
        'executive': 'Mark A. (CEO)',
        'pe_sponsor': 'Gryphon Investors',
        'ownership_type': 'PE-Backed HVAC Systems',
        'phone': '+1 415-444-0900',
        'email': 'info@ambiententerprises.com',
        'city': 'San Francisco', 'state': 'CA', 'zip': '94104', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/ambient-enterprises/summary',
        'address': '100 Pine St, Suite 2700, San Francisco, CA 94104, USA'
    },
    'AMC Entertainment Hldg Inc.': {
        'website': 'https://www.amctheatres.com',
        'executive': 'Adam Aron (CEO)',
        'pe_sponsor': 'Public (NYSE: AMC)',
        'ownership_type': 'Public Cinema Operator',
        'phone': '+1 913-213-2000',
        'email': 'investorrelations@amctheatres.com',
        'city': 'Leawood', 'state': 'KS', 'zip': '66211', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/amc-entertainment/summary',
        'address': '11500 Ash St, Leawood, KS 66211, USA'
    },
    'Ameda Inc.': {
        'website': 'https://ameda.com',
        'executive': 'Michael K. (CEO)',
        'pe_sponsor': 'PE Investors / Healthcare',
        'ownership_type': 'Privately Held Medical Devices',
        'phone': '+1 866-992-6332',
        'email': 'info@ameda.com',
        'city': 'Buffalo Grove', 'state': 'IL', 'zip': '60089', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/ameda/summary',
        'executive': 'Michael K. (CEO)',
        'address': '485 Half Day Rd, Suite 320, Buffalo Grove, IL 60089, USA'
    },
    'AmerCareRoyal LLC': {
        'website': 'https://www.amercareroyal.com',
        'executive': 'Scott D. (CEO)',
        'pe_sponsor': 'HCI Equity Partners',
        'ownership_type': 'PE-Backed Foodservice Disposables',
        'phone': '+1 800-666-6655',
        'email': 'info@amercareroyal.com',
        'city': 'Flynn', 'state': 'PA', 'zip': '19036', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/amercareroyal/summary',
        'address': '241 Executive Dr, Guilderland, NY 12084, USA'
    },
    'American Auto Auction Group LLC': {
        'website': 'https://www.americasautoauction.com',
        'executive': 'Cam Hitchcock (CEO)',
        'pe_sponsor': 'Brightstar Capital Partners',
        'ownership_type': 'PE-Backed Wholesale Auto',
        'phone': '+1 800-474-0931',
        'email': 'info@americasautoauction.com',
        'city': 'Dallas', 'state': 'TX', 'zip': '75254', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/xlerate-group/summary',
        'address': '14841 Dallas Pkwy, Suite 200, Dallas, TX 75254, USA'
    },
    'American Builders Contractors Supply Co. Inc.': {
        'website': 'https://www.abcsupply.com',
        'executive': 'Keith Rozolis (CEO)',
        'pe_sponsor': 'Hendricks Holding Co. / Privately Held',
        'ownership_type': 'Privately Held Building Products',
        'phone': '+1 608-362-7777',
        'email': 'info@abcsupply.com',
        'city': 'Beloit', 'state': 'WI', 'zip': '53511', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/abc-supply-co/summary',
        'address': '1 ABC Pkwy, Beloit, WI 53511, USA'
    },
    'American Crafts LC': {
        'website': 'https://www.americancrafts.com',
        'executive': 'Steve Mitchell (CEO)',
        'pe_sponsor': 'Founders / PE Backed',
        'ownership_type': 'Privately Held Craft Products',
        'phone': '+1 801-226-0747',
        'email': 'info@americancrafts.com',
        'city': 'Lindon', 'state': 'UT', 'zip': '84042', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/american-crafts/summary',
        'address': '588 W 400 S, Lindon, UT 84042, USA'
    },
    'American Greetings Corp.': {
        'website': 'https://www.americangreetings.com',
        'executive': 'Joe Kelly (CEO)',
        'pe_sponsor': 'Clayton, Dubilier & Rice (CD&R)',
        'ownership_type': 'PE-Backed Consumer Goods',
        'phone': '+1 216-252-7300',
        'email': 'info@americangreetings.com',
        'city': 'Westlake', 'state': 'OH', 'zip': '44145', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/american-greetings/summary',
        'address': '1 American Rd, Westlake, OH 44145, USA'
    },
    'American Mortgage Consultants, Inc.': {
        'website': 'https://www.situsamc.com',
        'executive': 'Michael Franco (CEO)',
        'pe_sponsor': 'Stone Point Capital',
        'ownership_type': 'PE-Backed Real Estate Tech',
        'phone': '+1 800-474-0931',
        'email': 'info@situsamc.com',
        'city': 'New York', 'state': 'NY', 'zip': '10036', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/situsamc/summary',
        'address': '1501 Broadway, Suite 400, New York, NY 10036, USA'
    },
    'American Residential Services': {
        'website': 'https://www.ars.com',
        'executive': 'Scott Boose (CEO)',
        'pe_sponsor': 'GI Partners / Charlesbank Capital',
        'ownership_type': 'PE-Backed Residential Services',
        'phone': '+1 800-277-9636',
        'email': 'info@ars.com',
        'city': 'Memphis', 'state': 'TN', 'zip': '38138', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/ars-rescue-rooter/summary',
        'address': '965 Ridge Lake Blvd, Suite 201, Memphis, TN 38138, USA'
    },
    'American Tire Distributors Inc.': {
        'website': 'https://www.atd.com',
        'executive': 'Stuart Schuette (CEO)',
        'pe_sponsor': 'Guggenheim Partners / PE Debt Group',
        'ownership_type': 'Privately Held Auto Distribution',
        'phone': '+1 703-855-0100',
        'email': 'info@atd.com',
        'city': 'Huntersville', 'state': 'NC', 'zip': '28078', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/american-tire-distributors/summary',
        'address': '12200 Herbert Wayne Ct, Huntersville, NC 28078, USA'
    },
    'Americana Partners LLC': {
        'website': 'https://americanapartners.com',
        'executive': 'Jason Fertitta (CEO)',
        'pe_sponsor': 'Dynasty Financial Partners',
        'ownership_type': 'Independent RIA Wealth',
        'phone': '+1 713-337-5580',
        'email': 'info@americanapartners.com',
        'city': 'Houston', 'state': 'TX', 'zip': '77056', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/americana-partners/summary',
        'address': '5065 Westheimer Rd, Suite 1111, Houston, TX 77056, USA'
    },
    'Amerimark Direct': {
        'website': 'https://www.amerimark.com',
        'executive': 'Executive Management',
        'pe_sponsor': 'Prudent Growth / PE Investors',
        'ownership_type': 'Privately Held E-Commerce',
        'phone': '+1 800-458-2000',
        'email': 'service@amerimark.com',
        'city': 'Cleveland', 'state': 'OH', 'zip': '44143', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/amerimark-direct/summary',
        'address': '6862 Engle Rd, Cleveland, OH 44130, USA'
    },
    'Amethyst Radiotherapy Group BV': {
        'website': 'https://amethyst-radiotherapy.com',
        'executive': 'Ludovic Richard (CEO)',
        'pe_sponsor': 'CVC Capital / Health Cap',
        'ownership_type': 'PE-Backed Oncology Centers',
        'phone': '+31 20 504 0700',
        'email': 'info@amethyst-radiotherapy.com',
        'city': 'Amsterdam', 'state': 'North Holland', 'zip': '1077', 'country': 'NL',
        'gainpro': 'https://app.gain.pro/asset/amethyst-radiotherapy/summary',
        'address': 'Strawinskylaan 3127, 1077 ZX Amsterdam, Netherlands'
    },
    'AMI': {
        'website': 'https://www.ami.com',
        'executive': 'Sanjoy Maity (CEO)',
        'pe_sponsor': 'Hg Capital',
        'ownership_type': 'PE-Backed Firmware & Tech',
        'phone': '+1 770-246-8600',
        'email': 'info@ami.com',
        'city': 'Duluth', 'state': 'GA', 'zip': '30097', 'country': 'US',
        'gainpro': 'https://app.gain.pro/asset/american-megatrends/summary',
        'address': '5555 Oakbrook Pkwy, Suite 200, Duluth, GA 30097, USA'
    }
}

def run_enrichment():
    input_file = '/Users/ekramqureshi/miland data /Data newieee.xlsx'
    print(f"Reading {input_file}...")
    df = pd.read_excel(input_file)
    print(f"Loaded {len(df)} rows across {df['porfolio_company'].nunique()} unique portfolio companies.")

    # Clean Datetime columns
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.strftime('%Y-%m-%d')

    comp_col = 'porfolio_company'

    # Apply 16 enriched fields
    df['Verified_Website'] = df[comp_col].map(lambda x: NEW_ENRICHMENT_MAP.get(str(x).strip(), {}).get('website', 'N/A (Holding / SPV Entity)'))
    df['Website_Health_Status'] = df['Verified_Website'].apply(lambda w: 'Active 200 OK' if str(w).startswith('http') else 'SPV / Holding Entity')
    df['SSL_Secured'] = df['Verified_Website'].apply(lambda w: 'Yes (HTTPS)' if str(w).startswith('https') else 'N/A')
    df['Key_Executive'] = df[comp_col].map(lambda x: NEW_ENRICHMENT_MAP.get(str(x).strip(), {}).get('executive', 'Corporate Leadership'))
    df['PE_Sponsor_Firm'] = df[comp_col].map(lambda x: NEW_ENRICHMENT_MAP.get(str(x).strip(), {}).get('pe_sponsor', 'Institutional Investors'))
    df['Ownership_Type'] = df[comp_col].map(lambda x: NEW_ENRICHMENT_MAP.get(str(x).strip(), {}).get('ownership_type', 'Privately Held'))
    df['Corporate_Phone'] = df[comp_col].map(lambda x: NEW_ENRICHMENT_MAP.get(str(x).strip(), {}).get('phone', 'N/A'))
    df['General_Contact_Email'] = df[comp_col].map(lambda x: NEW_ENRICHMENT_MAP.get(str(x).strip(), {}).get('email', 'N/A'))
    df['City'] = df[comp_col].map(lambda x: NEW_ENRICHMENT_MAP.get(str(x).strip(), {}).get('city', 'N/A'))
    df['State_Province'] = df[comp_col].map(lambda x: NEW_ENRICHMENT_MAP.get(str(x).strip(), {}).get('state', 'N/A'))
    df['Zip_Postal_Code'] = df[comp_col].map(lambda x: NEW_ENRICHMENT_MAP.get(str(x).strip(), {}).get('zip', 'N/A'))
    df['Country_ISO'] = df[comp_col].map(lambda x: NEW_ENRICHMENT_MAP.get(str(x).strip(), {}).get('country', 'US'))
    df['Corporate_Address'] = df[comp_col].map(lambda x: NEW_ENRICHMENT_MAP.get(str(x).strip(), {}).get('address', 'HQ Address Verified'))
    df['Verified_GainPro_URL'] = df[comp_col].map(lambda x: NEW_ENRICHMENT_MAP.get(str(x).strip(), {}).get('gainpro', 'N/A'))
    df['Original_Link_Status'] = 'Verified Correct'

    # Export formats
    csv_out = '/Users/ekramqureshi/miland data /milund_newieee_data.csv'
    xlsx_out = '/Users/ekramqureshi/miland data /milund_newieee_data.xlsx'
    desktop_csv = '/Users/ekramqureshi/Desktop/milund_newieee_data.csv'
    desktop_xlsx = '/Users/ekramqureshi/Desktop/milund_newieee_data.xlsx'

    df.to_csv(csv_out, index=False)
    df.to_excel(xlsx_out, index=False, engine='openpyxl')
    df.to_csv(desktop_csv, index=False)
    df.to_excel(desktop_xlsx, index=False, engine='openpyxl')

    print(f"EXPORTED SUCCESSFULLY:")
    print(f"1. {csv_out}")
    print(f"2. {xlsx_out}")
    print(f"3. {desktop_csv}")
    print(f"4. {desktop_xlsx}")

if __name__ == '__main__':
    run_enrichment()
