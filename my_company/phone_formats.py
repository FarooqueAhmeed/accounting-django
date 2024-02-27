phone_formats = {
    '+1': r'^\d{10}$',  # United States (10 digits)
    '+20': r'^\d{8,11}$',  # Egypt (8 to 11 digits)
    '+27': r'^\d{9,10}$',  # South Africa (9 or 10 digits)
    '+30': r'^\d{10}$',  # Greece (10 digits)
    '+31': r'^\d{9,10}$',  # Netherlands (9 or 10 digits)
    '+32': r'^\d{8,9}$',  # Belgium (8 or 9 digits)
    '+33': r'^\d{9}$',  # France (9 digits)
    '+34': r'^\d{9}$',  # Spain (9 digits)
    '+36': r'^\d{9}$',  # Hungary (9 digits)
    '+39': r'^\d{6,12}$',  # Italy (6 to 12 digits)
    '+40': r'^\d{9}$',  # Romania (9 digits)
    '+41': r'^\d{9,10}$',  # Switzerland (9 or 10 digits)
    '+43': r'^\d{9}$',  # Austria (9 digits)
    '+44': r'^\d{10,11}$',  # United Kingdom (10 or 11 digits)
    '+45': r'^\d{8}$',  # Denmark (8 digits)
    '+46': r'^\d{7,10}$',  # Sweden (7 to 10 digits)
    '+47': r'^\d{8,12}$',  # Norway (8 to 12 digits)
    '+48': r'^\d{9}$',  # Poland (9 digits)
    '+49': r'^\d{6,13}$',  # Germany (6 to 13 digits)
    '+51': r'^\d{9}$',  # Peru (9 digits)
    '+52': r'^\d{7,13}$',  # Mexico (7 to 13 digits)
    '+53': r'^\d{6,8}$',  # Cuba (6 to 8 digits)
    '+54': r'^\d{10}$',  # Argentina (10 digits)
    '+55': r'^\d{10,11}$',  # Brazil (10 or 11 digits)
    '+56': r'^\d{8,9}$',  # Chile (8 or 9 digits)
    '+57': r'^\d{10}$',  # Colombia (10 digits)
    '+58': r'^\d{7,10}$',  # Venezuela (7 to 10 digits)
    '+60': r'^\d{9,10}$',  # Malaysia (9 or 10 digits)
    '+61': r'^\d{8,10}$',  # Australia (8 to 10 digits)
    '+62': r'^\d{9,12}$',  # Indonesia (9 to 12 digits)
    '+63': r'^\d{7,12}$',  # Philippines (7 to 12 digits)
    '+64': r'^\d{8,9}$',  # New Zealand (8 or 9 digits)
    '+65': r'^\d{8}$',  # Singapore (8 digits)
    '+66': r'^\d{9,10}$',  # Thailand (9 or 10 digits)
    '+81': r'^\d{10}$',  # Japan (10 digits)
    '+82': r'^\d{8,11}$',  # South Korea (8 to 11 digits)
    '+84': r'^\d{8,12}$',  # Vietnam (8 to 12 digits)
    '+86': r'^\d{11}$',  # China (11 digits)
    '+90': r'^\d{10}$',  # Turkey (10 digits)
    '+91': r'^\d{10}$',  # India (10 digits)
    '+92': r'^\d{10}$',  # Pakistan (10 digits)
    '+93': r'^\d{7,8}$',  # Afghanistan (7 or 8 digits)
    '+94': r'^\d{9}$',  # Sri Lanka (9 digits)
    '+95': r'^\d{8}$',  # Myanmar (8 digits
        '+98': r'^\d{10}$',  # Iran (10 digits)
    '+211': r'^\d{9}$',  # South Sudan (9 digits)
    '+213': r'^\d{9}$',  # Algeria (9 digits)
    '+216': r'^\d{8}$',  # Tunisia (8 digits)
    '+218': r'^\d{9,10}$',  # Libya (9 or 10 digits)
    '+220': r'^\d{7,8}$',  # Gambia (7 or 8 digits)
    '+221': r'^\d{9}$',  # Senegal (9 digits)
    '+222': r'^\d{7}$',  # Mauritania (7 digits)
    '+223': r'^\d{8}$',  # Mali (8 digits)
    '+224': r'^\d{8}$',  # Guinea (8 digits)
    '+225': r'^\d{8}$',  # Ivory Coast (8 digits)
    '+226': r'^\d{8}$',  # Burkina Faso (8 digits)
    '+227': r'^\d{8}$',  # Niger (8 digits)
    '+228': r'^\d{8}$',  # Togo (8 digits)
    '+229': r'^\d{8}$',  # Benin (8 digits)
    '+230': r'^\d{7}$',  # Mauritius (7 digits)
    '+231': r'^\d{7}$',  # Liberia (7 digits)
    '+232': r'^\d{8}$',  # Sierra Leone (8 digits)
    '+233': r'^\d{8}$',  # Ghana (8 digits)
    '+234': r'^\d{10}$',  # Nigeria (10 digits)
    '+235': r'^\d{8}$',  # Chad (8 digits)
    '+236': r'^\d{8}$',  # Central African Republic (8 digits)
    '+237': r'^\d{8,9}$',  # Cameroon (8 or 9 digits)
    '+238': r'^\d{7}$',  # Cape Verde (7 digits)
    '+239': r'^\d{7}$',  # Sao Tome and Principe (7 digits)
    '+240': r'^\d{7,8}$',  # Equatorial Guinea (7 or 8 digits)
    '+241': r'^\d{7}$',  # Gabon (7 digits)
    '+242': r'^\d{7}$',  # Republic of the Congo (7 digits)
    '+243': r'^\d{9}$',  # Democratic Republic of the Congo (9 digits)
    '+244': r'^\d{9}$',  # Angola (9 digits)
    '+245': r'^\d{7}$',  # Guinea-Bissau (7 digits)
    '+246': r'^\d{4}$',  # British Indian Ocean Territory (4 digits)
    '+247': r'^\d{4}$',  # Ascension Island (4 digits)
    '+248': r'^\d{7}$',  # Seychelles (7 digits)
    '+249': r'^\d{9}$',  # Sudan (9 digits)
    '+250': r'^\d{9}$',  # Rwanda (9 digits)
    '+251': r'^\d{9}$',  # Ethiopia (9 digits)
    '+252': r'^\d{8}$',  # Somalia (8 digits)
    '+253': r'^\d{7}$',  # Djibouti (7 digits)
    '+254': r'^\d{9}$',  # Kenya (9 digits)
    '+255': r'^\d{9}$',  # Tanzania (9 digits)
    '+256': r'^\d{9}$',  # Uganda (9 digits)
    '+257': r'^\d{8}$',  # Burundi (8 digits)
    '+258': r'^\d{9}$',  # Mozambique (9 digits)
    '+260': r'^\d{9}$',  # Zambia (9 digits)
    '+261': r'^\d{9}$',  # Madagascar (9 digits)
    '+262': r'^\d{9}$',  # Reunion (9 digits)
    '+263': r'^\d{9}$',  # Zimbabwe (9 digits)
    '+264': r'^\d{7,8}$',  # Namibia (7 or 8 digits)
    '+265': r'^\d{7,9}$',  # Malawi (7 to 9 digits)
    '+266': r'^\d{8}$',  # Lesotho (8 digits)
    '+267': r'^\d{8}$',  # Botswana (8 digits)
    '+268': r'^\d{7}$',  # Eswatini (7 digits)
    '+269': r'^\d{7}$',  # Comoros (7 digits)
    '+290': r'^\d{4}$',  # Saint Helena (4 digits)
    '+291': r'^\d{7}$',  # Eritrea (7 digits)
    '+297': r'^\d{7}$',  # Aruba (7 digits)
    '+298': r'^\d{6}$',  # Faroe Islands (6 digits)
    '+299': r'^\d{6}$',  # Greenland (6 digits)
    '+350': r'^\d{8}$',  # Gibraltar (8 digits)
    '+351': r'^\d{9}$',  # Portugal (9 digits)
    '+352': r'^\d{6,7}$',  # Luxembourg (6 or 7 digits)
    '+353': r'^\d{7,8}$',  # Ireland (7 or 8 digits)
    '+354': r'^\d{7}$',  # Iceland (7 digits)
    '+355': r'^\d{9}$',  # Albania (9 digits)
    '+356': r'^\d{8}$',  # Malta (8 digits)
    '+357': r'^\d{8}$',  # Cyprus (8 digits)
    '+358': r'^\d{5,12}$',  # Finland (5 to 12 digits)
    '+359': r'^\d{8,10}$',  # Bulgaria (8 to 10 digits)
    '+370': r'^\d{8}$',  # Lithuania (8 digits)
    '+371': r'^\d{8,9}$',  # Latvia (8 or 9 digits)
    '+372': r'^\d{7,8}$',  # Estonia (7 or 8 digits)
    '+373': r'^\d{8}$',  # Moldova (8 digits)
    '+374': r'^\d{8}$',  # Armenia (8 digits)
    '+375': r'^\d{9}$',  # Belarus (9 digits)
    '+376': r'^\d{6}$',  # Andorra (6 digits)
    '+377': r'^\d{8}$',  # Monaco (8 digits)
    '+378': r'^\d{5}$',  # San Marino (5 digits)
    '+380': r'^\d{9}$',  # Ukraine (9 digits)
    '+381': r'^\d{8}$',  # Serbia (8 digits)
    '+382': r'^\d{7,8}$',  # Montenegro (7 or 8 digits)
    '+383': r'^\d{7}$',  # Kosovo (7 digits)
    '+385': r'^\d{8}$',  # Croatia (8 digits)
    '+386': r'^\d{8}$',  # Slovenia (8 digits)
    '+387': r'^\d{8}$',  # Bosnia and Herzegovina (8 digits)
    '+389': r'^\d{8,9}$',  # North Macedonia (8 or 9 digits)
    '+420': r'^\d{9}$',  # Czech Republic (9 digits)
    '+421': r'^\d{7}$',  # Slovakia (7 digits)
    '+423': r'^\d{6}$',  # Liechtenstein (6 digits)
    '+500': r'^\d{5}$',  # Falkland Islands (5 digits)
    '+501': r'^\d{7}$',  # Belize (7 digits)
    '+502': r'^\d{8}$',  # Guatemala (8 digits)
    '+503': r'^\d{8}$',  # El Salvador (8 digits)
    '+504': r'^\d{7}$',  # Honduras (7 digits)
    '+505': r'^\d{8}$',  # Nicaragua (8 digits)
    '+506': r'^\d{8}$',  # Costa Rica (8 digits)
    '+507': r'^\d{8}$',  # Panama (8 digits)
    '+508': r'^\d{6}$',  # Saint Pierre and Miquelon (6 digits)
    '+509': r'^\d{8}$',  # Haiti (8 digits)
    '+590': r'^\d{9}$',  # Guadeloupe (9 digits)
    '+591': r'^\d{7,8}$',  # Bolivia (7 or 8 digits)
    '+592': r'^\d{7}$',  # Guyana (7 digits)
    '+593': r'^\d{9}$',  # Ecuador (9 digits)
    '+594': r'^\d{9}$',  # French Guiana (9 digits)
    '+595': r'^\d{8}$',  # Paraguay (8 digits)
    '+596': r'^\d{9}$',  # Martinique (9 digits)
    '+597': r'^\d{7}$',  # Suriname (7 digits)
    '+598': r'^\d{7}$',  # Uruguay (7 digits)
    '+599': r'^\d{7}$',  # Caribbean Netherlands (7 digits)
    '+670': r'^\d{7}$',  # East Timor (7 digits)
    '+672': r'^\d{4}$',  # Norfolk Island (4 digits)
    '+673': r'^\d{6}$',  # Brunei (6 digits)
    '+674': r'^\d{4}$',  # Nauru (4 digits)
    '+675': r'^\d{7}$',  # Papua New Guinea (7 digits)
    '+676': r'^\d{7}$',  # Tonga (7 digits)
    '+677': r'^\d{7}$',  # Solomon Islands (7 digits)
    '+678': r'^\d{4,5}$',  # Vanuatu (4 or 5 digits)
    '+679': r'^\d{5,7}$',  # Fiji (5 to 7 digits)
    '+680': r'^\d{7}$',  # Palau (7 digits)
    '+681': r'^\d{6}$',  # Wallis and Futuna (6 digits)
    '+682': r'^\d{4}$',  # Cook Islands (4 digits)
    '+683': r'^\d{4}$',  # Niue (4 digits)
    '+685': r'^\d{7}$',  # Samoa (7 digits)
    '+686': r'^\d{6}$',  # Kiribati (6 digits)
    '+687': r'^\d{6}$',  # New Caledonia (6 digits)
    '+688': r'^\d{6}$',  # Tuvalu (6 digits)
    '+689': r'^\d{6}$',  # French Polynesia (6 digits)
    '+690': r'^\d{4}$',  # Tokelau (4 digits)
    '+691': r'^\d{7}$',  # Micronesia (7 digits)
    '+692': r'^\d{7}$',  # Marshall Islands (7 digits)
    '+850': r'^\d{10}$',  # North Korea (10 digits)
    '+852': r'^\d{8}$',  # Hong Kong (8 digits)
    '+853': r'^\d{8}$',  # Macau (8 digits)
    '+855': r'^\d{7,8}$',  # Cambodia (7 or 8 digits)
    '+880': r'^\d{9,10}$',  # Bangladesh (9 or 10 digits)
    '+886': r'^\d{9}$',  # Taiwan (9 digits)
    '+960': r'^\d{7}$',  # Maldives (7 digits)
    '+961': r'^\d{7,8}$',  # Lebanon (7 or 8 digits)
    '+962': r'^\d{6,8}$',  # Jordan (6 to 8 digits)
    '+963': r'^\d{7,8}$',  # Syria (7 or 8 digits)
    '+964': r'^\d{10}$',  # Iraq (10 digits)
    '+965': r'^\d{8}$',  # Kuwait (8 digits)
    '+966': r'^\d{9}$',  # Saudi
    '+966': r'^\d{9}$',  # Saudi Arabia (9 digits)
    '+967': r'^\d{7,9}$',  # Yemen (7 to 9 digits)
    '+968': r'^\d{8}$',  # Oman (8 digits)
    '+970': r'^\d{7,8}$',  # Palestine (7 or 8 digits)
    '+971': r'^\d{9}$',  # United Arab Emirates (9 digits)
    '+972': r'^\d{7}$',  # Israel (7 digits)
    '+973': r'^\d{7}$',  # Bahrain (7 digits)
    '+974': r'^\d{7}$',  # Qatar (7 digits)
    '+975': r'^\d{7}$',  # Bhutan (7 digits)
    '+976': r'^\d{7,8}$',  # Mongolia (7 or 8 digits)
}


