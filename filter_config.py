"""
Configuration for filtering Hindi daily TV serials and protecting legitimate web series and movies.
"""

# TMDB TV Genre IDs to exclude for television content
EXCLUDED_TV_GENRES = {
    10763,  # News
    10764,  # Reality
    10766,  # Soap (Soap Opera)
    10767   # Talk
}

# Known Hindi daily serials by TMDB ID
KNOWN_SERIAL_IDS = {
    75254,   # Dil Se Dil Tak
    242384,  # Chookar Mere Maan Ko
    75235,   # Yeh Un Dinon Ki Baat Hai
    75282,   # Kundali Bhagya
    112444,  # Saath Nibhaana Saathiya 2
    87655,   # Yeh Rishtey Hain Pyaar Ke
    242896,  # Kyunki Saas Maa Bahu Beti Hoti Hai
    241810,  # Kavya - Ek Jazbaa, Ek Junoon
    15662,   # Kahaani Hamaaray Mahaabhaarat Ki
    126520,  # Ek Bhram - Sarvagun Sampanna
    75247,   # Savitri Devi College & Hospital
    42267,   # Main Lakshmi Tere Aangan Ki
    14837,   # Kuchh Is Tara
    309802,  # Tere Sheher Mein
    1275,    # Astitva...Ek Prem Kahani
    8253,    # Kabhie To Nazar Milao
    38883,   # Ganga Kii Dheej
    137721,  # Rishton Ka Manjha
    44311,   # Aasman Se Aage
    283893,  # Tera Yaar Hoon Main
    319145,  # Hara Sindoor
    113835,  # Brahmarakshas
    211561,  # Imlie
    8530,    # Uttaran
    216498,  # Dheere Dheere Se
    259082,  # Mishri
    224643,  # Amma Ke Babu Ki Baby
    85088,   # Main Maike Chali Jaungi Tum Dekhte Rahiyo
    242574,  # Aangan Aapno Kaa
    239246,  # Pashminna – Dhaage Mohabbat Ke
    157785,  # Kaamnaa
    123565,  # Ishk Par Zor Nahi
    277944,  # Yes Boss
    15778,   # Alif Laila
    224349,  # Hum Rahe Na Rahe Hum
    8022,    # Kahe Naa Kahe
    115588,  # Karn Sangini
    224837,  # Sapnon Ki Chhalaang
    111805,  # Apna Time Bhi Aayega
    18486,   # Pavitra Rishta
    99811,   # Qurbaan Hua
    8368,    # Shree
    17356,   # Life Partner / Jeevan Saathi
    13949,   # Karam Apnaa Apnaa
    44839,   # Shubh Vivah
    8478,    # Shagun
    32474,   # Sajan Re Jhoot Mat Bolo
    4008,    # Kayamath
    8046,    # Kehta Hai Dil
    15324,   # Kabhii Sautan Kabhii Sahelii
    59377,   # Jeannie Aur Juju
    15174,   # Ye Meri Life Hai
    32360,   # Gutur Gu
    319143,  # Kyunki Rishton Ke Bhi Roop Badalte Hain
    42362,   # Kya Huaa Tera Vaada
    41933,   # Hitler Didi
    7689,    # Kyaa Hoga Nimmo Kaa
    21550,   # Maat Pitaah Ke Charnon Mein Swarg
    57762,   # Dhadkan
    8474,    # Jaane Kya Baat Hui
    60368,   # Kehta Hai Dil Jee Le Zara
    31396,   # Bairi Piya
    42270,   # Na Bole Tum Na Maine Kuch Kaha
    42126,   # Chidiya Ghar
    30805,   # 12/24 Karol Bagh
    34370,   # Dil Se Diya Vachan
    42114,   # Chintu Chinki Aur Ek Badi Si Love Story
    38196,   # Pyaar Mein Twist
    15544,   # Kya Aap Paanchvi Pass Se Tez Hain?
    99890,   # Bahu Hamari Rajni Kant
    75290,   # Badho Bahu
    39195,   # Ek Nayi Chhoti Si Zindagi
    8182,    # Simply Shekhar
    42108,   # R. K. Laxman Ki Duniya
    335329,  # Ring Wrong Ring
    34258,   # Aise Karo Naa Vidaa
    15314,   # Durgesh Nandinii
    34384,   # Saas Bina Sasural
    8494,    # Kaisa Ye Pyar Hai
    335787,  # Family Full House with Rohit Sharma
    257530,  # Laughter Chefs Unlimited Entertainment
    8745,    # Balika Vadhu
    58934,   # Bani – Ishq Da Kalma
    41761,   # Bitto
    3901,    # Baa Bahoo Aur Baby
    14110,   # Amber Dhara
    17568,   # Arzoo Hai Tu
    8159,    # Devi
    243787,  # Zindagi Abhi Baki Hai Mere Ghost
    115562,  # Lockdown Ki Love Story
    78451,   # Prithvi Vallabh
    101226,  # Maharaj Ki Jai Ho
    17531,   # Kya Dill Mein Hai
    7524,    # 10 Ka Dum
    14307,   # Aahat
    244291,  # Aankh Micholi
    155962,  # Achanak 37 Saal Baad
    34522,   # Adaalat
    261149,  # Advocate Anjali Awasthi
    17977,   # Agle Janam Mohe Bitiya Hi Kijo
    84982,   # Aladdin - Naam Toh Suna Hoga
    331932,  # Ali Baba Aur 40 Bhoot
    60334,   # Baalveer
    222610,  # Baalveer
    93456,   # Baalveer
    313155,  # Badi Doooor Se Aaye Hai
    245976,  # Baghin
    3986,    # Dekh Bhai Dekh
    82664,   # Savdhaan India
    100787,  # Savdhaan India - F.I.R.
    40030,   # Naagin
    75027,   # Naagin
    113063,  # Molkki
    82813,   # Guddan - Tumse Na Ho Payega
    217730,  # Dhruv Tara - Samay Sadi Se Pare
    226500,  # Shiv Shakti - Tap Tyaag Tandav
    219150,  # Maitree
    86153,   # Bhakharwadi
    42858,   # Dil Se Di Dua... Saubhagyavati Bhava?
    124110,  # Mauka-E-Vardaat
    104930,  # Crime Patrol Dial 100
    25883,   # Crime Patrol
    25880,   # C.I.D.
    13904,   # Kasautii Zindagii Kay
    82737,   # Kasautii Zindagii Kay
    1307,    # Kasauti Zindagii Kay
    42250,   # Bade Achhe Lagte Hain
    130090,  # Bade Achhe Lagte Hain 2
    225570,  # Bade Achhe Lagte Hain 3
    60118,   # Brave Son of India: Maharana Pratap
    280010,  # Kyunki Saas Bhi Kabhi Bahu Thi
    280011,  # Kahaani Ghar Ghar Kii
    96440,   # Yeh Rishta Kya Kehlata Hai
    105260,  # Anupamaa
    61222,   # Kumkum Bhagya
    111000,  # Ghum Hai Kisikey Pyaar Meiin
    130830,  # Bhagya Lakshmi
    32665,   # Taarak Mehta Ka Ooltah Chashmah
    62550,   # Diya Aur Baati Hum
    65750,   # Bhabiji Ghar Par Hain!
    42211,   # Sasural Simar Ka
    121000,  # Sasural Simar Ka 2
    60500,   # Yeh Hai Mohabbatein
    70000,   # Ishqbaaaz
    72000,   # Bepannah
    116000,  # Udaariyaan
    103553,  # Yeh Hai Chahatein
    94783,   # Yehh Jadu Hai Jinn Ka!
    75283,   # Woh Apna Sa
    15317,   # Zaara
    106765,  # Zindagi Ki Mehek
    94291,   # Swaragini
    205024,  # Swaran Ghar
    255264,  # Suhagan Chudail
    224201,  # Suryaputra Karn
    72996,   # Tashan-E-Ishq
    133212,  # Tera Mera Saath Rahe
    220309,  # Tere Ishq Mein Ghayal
    215103,  # Teri Meri Doriyaann
    228093,  # Titlie
    75230,   # Vighnaharta Ganesh
    286996,  # Veer Hanuman - Bolo Bajrang Bali Ki Jai
    138863,  # Sirf Tum
    19243,   # Son Pari
    15993,   # Ssshhhh...Koi Hai
    115765,  # Sumit Sambhal Lega
    195797,  # Spy Bahu
    315195,  # Trideviyaan
    331610,  # Yaro Ka Tashan
    328817,  # Yeh Fitoor Tera
    240293,  # Jhanak
    124460,  # Punyashlok Ahilyabai
    85879,   # Patiala Babes
    203769,  # Pushpa Impossible
    42316,   # Devon Ke Dev...Mahadev
    60698,   # Comedy Nights with Kapil
    83985,   # Chandragupta Maurya
    211088,  # Sherdil Shergill
    31210,   # Lapataganj
    91073,   # Choti Sarrdaarni
    210924,  # Harphoul Mohini
    293455,  # Noyontara
    15246,   # Jassi Jaissi Koi Nahin
    302431,  # Reporters
    133985,  # Prem Bandhan
    86634,   # Manmohini
    242722,  # Shrimad Ramayan
    46935    # Qubool Hai
}

# Known Hindi daily serial titles and normalized patterns
KNOWN_SERIAL_TITLES = {
    "dil se dil tak",
    "chookar mere maan ko",
    "yeh un dinon ki baat hai",
    "anupamaa",
    "anupama",
    "yeh rishta kya kehlata hai",
    "kumkum bhagya",
    "kundali bhagya",
    "ghum hai kisikey pyaar meiin",
    "ghum hai kisikey pyaar mein",
    "taarak mehta ka ooltah chashmah",
    "tarak mehta ka ooltah chasma",
    "bhagya lakshmi",
    "saath nibhaana saathiya",
    "saath nibhaana saathiya 2",
    "saath nibhana saathiya",
    "yeh rishtey hain pyaar ke",
    "kyunki saas maa bahu beti hoti hai",
    "kyunki saas bhi kabhi bahu thi",
    "kahaani ghar ghar kii",
    "kahani ghar ghar ki",
    "kasautii zindagii kay",
    "kasauti zindagi kay",
    "kasauti zindagii kay",
    "kavya ek jazbaa ek junoon",
    "kahaani hamaaray mahaabhaarat ki",
    "ek bhram sarvagun sampanna",
    "savitri devi college hospital",
    "main lakshmi tere aangan ki",
    "kuchh is tara",
    "tere sheher mein",
    "astitva ek prem kahani",
    "kabhie to nazar milao",
    "ganga kii dheej",
    "rishton ka manjha",
    "aasman se aage",
    "tera yaar hoon main",
    "hara sindoor",
    "brahmarakshas",
    "brahmarakshas jaag utha shaitan",
    "imlie",
    "uttaran",
    "dheere dheere se",
    "mishri",
    "amma ke babu ki baby",
    "main maike chali jaungi tum dekhte rahiyo",
    "aangan aapno kaa",
    "pashminna dhaage mohabbat ke",
    "kaamnaa",
    "ishk par zor nahi",
    "yes boss",
    "alif laila",
    "hum rahe na rahe hum",
    "kahe naa kahe",
    "karn sangini",
    "sapnon ki chhalaang",
    "apna time bhi aayega",
    "pavitra rishta",
    "qurbaan hua",
    "shree",
    "life partner",
    "jeevan saathi humsafar zindagi ke",
    "karam apnaa apnaa",
    "shubh vivah",
    "shagun",
    "sajan re jhoot mat bolo",
    "kayamath",
    "kehta hai dil",
    "kabhii sautan kabhii sahelii",
    "jeannie aur juju",
    "ye meri life hai",
    "gutur gu",
    "kyunki rishton ke bhi roop badalte hain",
    "kya huaa tera vaada",
    "hitler didi",
    "kyaa hoga nimmo kaa",
    "maat pitaah ke charnon mein swarg",
    "dhadkan",
    "jaane kya baat hui",
    "kehta hai dil jee le zara",
    "bairi piya",
    "na bole tum na maine kuch kaha",
    "chidiya ghar",
    "12 24 karol bagh",
    "dil se diya vachan",
    "chintu chinki aur ek badi si love story",
    "pyaar mein twist",
    "kya aap paanchvi pass se tez hain",
    "bahu hamari rajni kant",
    "badho bahu",
    "ek nayi chhoti si zindagi",
    "simply shekhar",
    "r k laxman ki duniya",
    "ring wrong ring",
    "aise karo naa vidaa",
    "durgesh nandinii",
    "saas bina sasural",
    "kaisa ye pyar hai",
    "family full house with rohit sharma",
    "laughter chefs unlimited entertainment",
    "balika vadhu",
    "bani ishq da kalma",
    "bitto",
    "baa bahoo aur baby",
    "amber dhara",
    "arzoo hai tu",
    "devi",
    "zindagi abhi baki hai mere ghost",
    "lockdown ki love story",
    "prithvi vallabh",
    "maharaj ki jai ho",
    "kya dill mein hai",
    "10 ka dum",
    "aahat",
    "aankh micholi",
    "achanak 37 saal baad",
    "adaalat",
    "advocate anjali awasthi",
    "agle janam mohe bitiya hi kijo",
    "aladdin naam toh suna hoga",
    "ali baba aur 40 bhoot",
    "baalveer",
    "badi doooor se aaye hai",
    "baghin",
    "dekh bhai dekh",
    "savdhaan india",
    "savdhaan india fir",
    "naagin",
    "molkki",
    "guddan tumse na ho payega",
    "dhruv tara samay sadi se pare",
    "shiv shakti tap tyaag tandav",
    "maitree",
    "bhakharwadi",
    "dil se di dua saubhagyavati bhava",
    "mauka e vardaat",
    "crime patrol",
    "crime patrol dial 100",
    "cid",
    "c i d",
    "bade achhe lagte hain",
    "bade achhe lagte hain 2",
    "bade achhe lagte hain 3",
    "brave son of india maharana pratap",
    "sasural simar ka",
    "sasural simar ka 2",
    "diya aur baati hum",
    "bhabiji ghar par hain",
    "bhabhiji ghar par hai",
    "yeh hai mohabbatein",
    "ishqbaaaz",
    "ishqbaaz",
    "bepannah",
    "bepannaah",
    "udaariyaan",
    "is pyaar ko kya naam doon",
    "iss pyaar ko kya naam doon",
    "kasam tere pyaar ki",
    "kullfi kumarr bajewala",
    "madhubala ek ishq ek junoon",
    "tujhse hai raabta",
    "shakti astitva ke ehsaas ki",
    "chhoti sarrdaarni",
    "choti sarrdaarni",
    "swaragini jodein rishton ke sur",
    "swaragini",
    "swaran ghar",
    "suhagan chudail",
    "suryaputra karn",
    "tashan e ishq",
    "tera mera saath rahe",
    "tere ishq mein ghayal",
    "teri meri doriyaann",
    "titlie",
    "vighnaharta ganesh",
    "veer hanuman bolo bajrang bali ki jai",
    "sirf tum",
    "son pari",
    "ssshhhh koi hai",
    "sumit sambhal lega",
    "spy bahu",
    "trideviyaan",
    "yaro ka tashan",
    "yeh fitoor tera",
    "jhanak",
    "punyashlok ahilyabai",
    "patiala babes",
    "pushpa impossible",
    "devon ke dev mahadev",
    "comedy nights with kapil",
    "chandragupta maurya",
    "sherdil shergill",
    "lapataganj",
    "harphoul mohini",
    "noyontara",
    "jassi jaissi koi nahin",
    "reporters",
    "prem bandhan",
    "manmohini",
    "shrimad ramayan",
    "qubool hai",
    "jodha akbar",
    "tenali rama",
    "beintehaa"
}

# Protected known Hindi web series titles (normalized)
KNOWN_WEB_SERIES_TITLES = {
    # Illustrative examples from specification
    "panchayat",
    "mirzapur",
    "mismatched",
    "the family man",
    "sacred games",
    "paatal lok",
    "pataal lok",

    # Acclaimed and popular Indian streaming originals
    "kota factory",
    "gullak",
    "delhi crime",
    "scam 1992",
    "scam 1992 the harshad mehta story",
    "scam 2003",
    "scam 2003 the telgi story",
    "rocket boys",
    "asur",
    "farzi",
    "guns gulaabs",
    "guns and gulaabs",
    "guns gulaabs",
    "jubilee",
    "kohrra",
    "special ops",
    "special ops 1 5 the himmat story",
    "taaza khabar",
    "breathe",
    "breathe into the shadows",
    "aarya",
    "dahaad",
    "cat",
    "rana naidu",
    "mai a mother s rage",
    "tooth pari when love bites",
    "aspirants",
    "tvf pitchers",
    "pitchers",
    "permanent roommates",
    "tripling",
    "tvf tripling",
    "college romance",
    "flames",
    "hostel daze",
    "sandwiched forever",
    "kaala paani",
    "the railway men",
    "the railway men the untold story of bhopal 1984",
    "bard of blood",
    "betaal",
    "ghoul",
    "leila",
    "selection day",
    "taj mahal 1989",
    "little things",
    "yeh kaali kaali ankhein",
    "she",
    "decoupled",
    "bombay begums",
    "the fame game",
    "fame game",
    "trial by fire",
    "scoop",
    "choona",
    "inspector rishi",
    "poacher",
    "lootere",
    "heeramandi",
    "heeramandi the diamond bazaar",
    "black warrant",
    "criminal justice",
    "criminal justice behind closed doors",
    "criminal justice adhura sach",
    "undekhi",
    "avrodh the siege within",
    "jl50",
    "jl 50",
    "tabbar",
    "maharani",
    "cubicles",
    "yeh meri family",
    "engineering girls",
    "immature",
    "saas bahu achaar pvt ltd",
    "saas bahu aur flamingo",
    "chacha vidhayak hain humare",
    "tandav",
    "mumbai diaries",
    "mumbai diaries 26 11",
    "afsos",
    "pushpavalli",
    "hasmukh",
    "bandish bandits",
    "modern love mumbai",
    "jee karda",
    "made in heaven",
    "tujhpe main fida",
    "badtameez dil",
    "gutar gu",
    "crushed",
    "dehati ladke",
    "half ca",
    "sandeep bhaiya",
    "tvf inmates",
    "tvf bachelors",
    "the aam aadmi family",
    "ncr days",
    "school friends class of 2026",
    "school friends",
    "campus diaries",
    "staff room",
    "sisterhood",
    "very parivarik",
    "happy family conditions apply",
    "sixer",
    "dhindora",
    "matsya kaand",
    "candy",
    "high",
    "grahan",
    "the whistleblower",
    "lalbazaar",
    "code m",
    "crackdown",
    "abhay",
    "aashram",
    "inside edge",
    "ray",
    "shehar lakhot",
    "call me bae",
    "brown",
    "daldal",
    "london files",
    "adrishyam the invisible heroes",
    "murshid",
    "the test case",
    "13 mussoorie",
    "24 india",
    "21 sarfarosh saragarhi 1897",
    "angry young men",
    "bad cop",
    "barun rai and the house on the cliff",
    "kaushiki",
    "tandoor",
    "hiccups hookups",
    "aadha ishq",
    "dil dosti dilemma",
    "dillogical",
    "tatlubaaz",
    "chidiya udd",
    "the married woman",
    "class",
    "sidehero",
    "home shanti",
    "house of secrets the burari deaths",
    "zindagi in short",
    "country mafia",
    "escaype live",
    "your honor in",
    "your honor",
    "the verdict state vs nanavati",
    "hundred",
    "fixerr",
    "thinkistan",
    "smoke",
    "kaafir",
    "out of love",
    "hostages",
    "the raikar case",
    "state of siege 26 11",
    "jeet ki zid",
    "bicchoo ka khel",
    "human",
    "rudra the edge of darkness",
    "bloody brothers",
    "the great indian murder",
    "ghar waapsi",
    "dr arora",
    "shiksha mandal",
    "faadu",
    "bambai meri jaan",
    "kafas",
    "the freelancer",
    "sultan of delhi",
    "the jengaburu curse",
    "killer soup",
    "indian police force",
    "karmma calling",
    "showtime",
    "ranneeti balakot beyond",
    "pill",
    "life hill gayi",
    "gyaarah gyaarah",
    "follow kar lo yaar",
    "raat jawaan hai",
    "do gubbare",
    "dude",
    "bachelors",
    "inmates",
    "girlfriend chor",
    "metro park",
    "almost together",
    "pehla pyaar less than 1 chance",
    "clean up company",
    "legacy",
    "gaming insaan",
    "carryminati",
    "aapka jags",
    "abhishek upmanyu",
    "raja rasoi aur anya kahaniyaan",
    "the discovery of india",
    "malgudi days",
    "byomkesh bakshi",
    "tamas",
    "bharat ek khoj",
    "ekaant",
    "sunflower",
    "taj divided by blood",
    "tanaav",
    "the night manager",
    "the office",
    "the empire",
    "the forgotten army",
    "tribhuvan mishra ca topper",
    "udan patolas",
    "unafraid",
    "untag",
    "untouchables",
    "virgin bhasskar",
    "woodpecker",
    "x x x unscripted",
    "x x x uncensored",
    "yudh",
    "zindabaad",
    "raakh",
    "matka king",
    "shaque trust no one",
    "waiting hai",
    "the revolutionaries",
    "chumbak",
    "operation safed sagar the untold story of the kargil war",
    "adarsh baal vidyalaya",
    "pritam and pedro",
    "glory",
    "kaptaan",
    "sankalp",
    "amar vishwas",
    "jaffna hills",
    "family kirana store",
    "taskaree the smuggler s web",
    "mrs deshpande",
    "single papa",
    "bhay the gaurav tiwari story",
    "perfect family",
    "ekaki",
    "perfect parents",
    "co ed",
    "the ba ds of bollywood",
    "the bastards of bollywood",
    "andhera",
    "khoj",
    "fittrat",
    "dev dd",
    "love bites",
    "bhaukaal",
    "broken but beautiful"
}

# Known web series TMDB IDs for guaranteed retention
KNOWN_WEB_SERIES_IDS = {
    101352,  # Panchayat
    84105,   # Mirzapur
    113457,  # Mismatched
    93352,   # The Family Man
    79352,   # Sacred Games
    103051,  # Paatal Lok
    100911,  # Asur
    132117,  # Farzi
    156714,  # Guns & Gulaabs
    100612,  # Special Ops
    138396,  # Special Ops 1.5 The Himmat Story
    201050,  # Dahaad
    158345,  # CAT
    124411,  # Aspirants
    114796,  # Tandav
    76659,   # Breathe
    104913,  # Aarya
    138211,  # Rocket Boys
    87508,   # Delhi Crime
    107588,  # Aashram
    87324,   # Abhay
    99109,   # Afsos
    261296,  # Angry Young Men
    84962,   # Apharan
    128217,  # Aranyak
    106581,  # Avrodh: The Siege Within
    88959,   # Baarish
    256522,  # Bad Cop
    228293,  # Badtameez Dil
    91016,   # Bard of Blood
    119148,  # Bombay Begums
    226560,  # Brown
    238108,  # Call Me Bae
    133028,  # Candy
    211116,  # Class
    97944,   # Code M
    214654,  # Country Mafia
    110249,  # Crackdown
    249766,  # Daldal
    275204,  # Dhindora
    249747,  # Dil Dosti Dilemma
    246489,  # Dillogical
    200822,  # Escaype Live
    127862,  # Grahan
    221566,  # Happy Family, Conditions Apply
    138621,  # Hiccups & Hookups
    111176,  # High
    199357,  # Home Shanti
    133359,  # House of Secrets: The Burari Deaths
    235356,  # Kaala Paani
    263374,  # Khalbali Records
    105022,  # Lalbazaar
    89545,   # Leila
    197989,  # London Files
    195900,  # Mai: A Mother's Rage
    138940,  # Matsya Kaand
    87275,   # Metro Park
    115466,  # Mumbai Diaries
    262154,  # Murshid
    206912,  # NCR Days
    120353,  # OK Computer
    260801,  # Pehla Pyaar - Less Than 1% Chance
    101955,  # Raja, Rasoi aur Anya Kahaniyaan
    205010,  # Saas Bahu Achaar Pvt. Ltd.
    224654,  # Saas, Bahu Aur Flamingo
    312794,  # School Friends Class of 2026
    226531,  # Scoop
    240322,  # Shehar Lakhot
    256538,  # Sisterhood
    214332,  # Sixer
    235612,  # Sultan Of Delhi
    75712,   # Tamas
    129736,  # Tandoor
    240291,  # Tatlubaaz
    90956,   # The Aam Aadmi Family
    120333,  # The Married Woman
    76793,   # The Test Case
    152429,  # The Whistleblower
    224333,  # Tooth Pari: When Love Bites
    76503,   # TVF Bachelors
    93104,   # TVF Inmates
    249601,  # Very Parivarik
    104663,  # Your Honor (IN)
    94144,   # The Verdict - State Vs Nanavati
    119408,  # Zindagi in Short
    15211,   # Malgudi Days
    63180,   # TVF Pitchers
    69710,   # TVF Tripling
    84454,   # Broken But Beautiful
    100732,  # Bhaukaal
    127332   # Sunflower
}

# Regex patterns matching Indian television broadcast channels / daily TV networks
TV_NETWORK_PATTERNS = [
    r"\bstar\s*plus\b",
    r"\bstar\s*bharat\b",
    r"\bstar\s*utsav\b",
    r"\bstar\s*jalsha\b",
    r"\bzee\s*tv\b",
    r"\bcolors\s*(?:tv)?\b",
    r"\bcolors\s*rishtey\b",
    r"\bsony\s*tv\b",
    r"\bsony\s*entertainment\s*television\b",
    r"\bset\s*india\b",
    r"\bsab\s*tv\b",
    r"\bsony\s*sab\b",
    r"\blife\s*ok\b",
    r"\bdangal\s*(?:tv)?\b",
    r"\bsahara\s*one\b",
    r"\bdd\s*national\b",
    r"\bdoordarshan\b",
    r"\bchannel\s*v\b",
    r"\bbindass\b",
    r"\bmtv\s*india\b",
    r"\b9x\b",
    r"\bimagine\s*tv\b",
    r"\bndtv\s*imagine\b",
    r"\b&tv\b",
    r"\bandtv\b",
    r"\bbig\s*magic\b",
    r"\bsun\s*neo\b"
]

# Daily soap / linear TV serial keywords & descriptive phrases
DAILY_SOAP_PATTERNS = [
    r"\bsoap\s*opera\b",
    r"\bdaily\s*soap\b",
    r"\bindian\s*soap\b",
    r"\btelenovela\b",
    r"\bmon(?:day)?\s*to\s*fri(?:day)?\b",
    r"\bmon(?:day)?\s*through\s*fri(?:day)?\b",
    r"\bmon-fri\b",
    r"\bmon\s*to\s*fri\b",
    r"\bdaily\s*television\b",
    r"\bdaily\s*serial\b",
    r"\bdaily\s*drama\b",
    r"\bsitcom\s*that\s*aired\s*on\b",
    r"\bproduced\s*by\s*balaji\s*telefilms\b",
    r"\bbalaji\s*telefilms\s*(?:presents|drama|serial|production)\b",
    r"\bbroadcast\s*on\s*(?:star\s*plus|zee\s*tv|colors|sony|sab\s*tv|life\s*ok)\b",
    r"\baired\s*on\s*(?:star\s*plus|zee\s*tv|colors|sony|sab\s*tv|life\s*ok|star\s*bharat)\b",
    r"\btelecast\s*on\s*(?:star|zee|colors|sony|sab\s*tv|sahara\s*one|life\s*ok)\b",
    r"\bindian\s*television\s*(?:drama|daily)\s*series\b",
    r"\btelevision\s*series\s*that\s*aired\s*on\b",
    r"\btelevision\s*soap\b"
]

# OTT platforms & streaming indicators (protected from accidental daily soap classification)
OTT_PLATFORM_PATTERNS = [
    r"\bnetflix\b",
    r"\bamazon\s*prime\b",
    r"\bprime\s*video\b",
    r"\bdisney\+\s*hotstar\b",
    r"\bhotstar\s*specials\b",
    r"\bhotstar\b",
    r"\bsonyliv\b",
    r"\bzee5\b",
    r"\bjiocinema\b",
    r"\bvoot\s*select\b",
    r"\bmx\s*player\b",
    r"\btvf\b",
    r"\bthe\s*viral\s*fever\b",
    r"\bdice\s*media\b",
    r"\bpocket\s*aces\b",
    r"\bfiltercopy\b",
    r"\blionsgate\s*play\b",
    r"\bamazon\s*minitv\b",
    r"\bminitv\b",
    r"\byoutube\s*original\b",
    r"\bweb\s*series\b",
    r"\bstreaming\s*series\b"
]
