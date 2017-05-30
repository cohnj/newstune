import re
import unicodedata
from pymongo import Connection
import cPickle as pickle
from utils import *
import math
from pareto import *
#from nltk.stem.snowball import SnowballStemmer


#CATEGORY LISTS

partisan = ["trump","lying","left","corrupt","liberal","islam","race","money","country","illegal",
			"hillary","bernie","republicans","nra","progressive","immigrant","wall","terrorist",
			"muslim","election","washington","debate","refugee","lyin","nasty","revolution","radical",
			"terrorism","rigged","alt-right","bigly","birther","breitbart","fake","divide","division",
			"wound","wing","brexit","isis","obama"]

business = ['capital','ceo','career','commerce','client','commodity','credit','bank','loan','finance',
			'invest','trade','co','co.','company','consumer','business','corporation','customer','distributor','employee','employees',
			'exporter','export','firm','investor','customer relationship','proprietor','revenue','trader','credit','manufacture',
			'assessor','auditor','banker','employer','businessmen','businessman','inc.','enterprise','e-business','e-commerce','ebusiness',
			'ecommerce','globalization','mass market','offshore','open market','private enterprise',
			'primary sector','secondary sector','vested interest']

# print len(business)
# from business import business
# print len(business)

success = ['accomplish','achieve','acquire','assure','attain','attainment','beat','comprehensive','conclusive','consensus','consummate','cream','crown','culminate','culmination',
			'cure','definitive','enhance','establish','fix','fruition','fulfill','fullness','gain','get','graduate','harvest','master','obtain','pass','perfect','perfection','pinnacle',
			'qualify','realize','recover','recovery','regain','succeed','success','successful','survive','sustain','top','triumph','win','won']

startups = ['accelerator','incubator','accredited','investor','advertorials','advertainment','bleeding edge','boot strapping','b2b','business to business','b2c','business to consumer',
			'burn rate','run rate','churn rate','cliff','cottage business','cottage industry','deck','pitch deck','disruptive technology','exit strategy','fma','first mover advantage','freemium',
			'gamify','growth hacking','hockey stick','ip','intellectual property','iterate','launch','lean startup','leverage','loss leader pricing','low hanging fruit','market penetration','monetize',
			'mvp','minimum viable product','pivot','ramen profitable','roi','return on investment','runway','saas','software as a service','scaleable','sweat equity','term sheet','sprint','traction',
			'valuation','value proposisition','vaporware','vc','venture capital','venture capitalist','startup','start-up','patron','stakeholder']

science = ['datum', 'scientist', 'scientists', 'physical science', 'microbiologist', 'lepidoptery', 'watch glass', 'thesis', 'doctrate', 'geology', 'astronomy',
			'entomology', 'dr.', 'evolution', 'immunology', 'volumetric flask', 'particle', 'bunsen burner', 'microscope', 'biological', 'mathematical', 'telescope',
			'test tube', 'laboratory', 'ichthyology', 'genetics', 'microbiology', 'philosopher', 'research', 'experiment', 'experiments', 'fossil', 'electronics',
			'math', 'biology', 'theory', 'physicist', 'magnetism', 'radiology', 'hypothesis', 'beaker', 'graduated cylinder', 'geometry',  'electricity', 'burette', 'experimental',
			'botany', 'mineralogy', 'philosophical', 'zoology', 'astronomy',  'temperature', 'cuvette', 'quantum mechanics', 'clinical', 'astrophysics',
			'funnel', 'educated', 'academy', 'meteorologist',  'geophysics', 'atom', 'physician', 'observatory', 'science', 'meteorology', 'electrochemist'
			, 'ornithology',  'volcanology', 'tissue', 'educational', 'biochemistry', 'paleontology', 'gravity', 'chemical',  'thermometer',
			'mathematics', 'climatologist', 'journal', 'pipette', 'molecule', 'lab', 'seismology', 'faculty',  'philosophic', 'virologist', 'herpetology',
			'petri dish', 'organism', 'chemistry', 'physics','chemist','biologist', 'discovery','invention','phd','hydrogen','superconductor','IEEE','discover','invent',
			'fossil','fossils','researcher','researchers']

failure = ['abandon','abandonment','absence','absent','absent-minded','absentee','aimless','astray','asunder','back','bail','balk','bankrupt','bankruptcy','blockhead','blunder',
			'bolt','break','breakdown','broke','buckle','calamity','capitulate','capsize','clog','default','delinquency','delinquent','destruction','disable','disappoint','disarm','dissatisfy',
			'droop','drop','drought','err','erroneous','fail','fiasco','flaw','flounder','foible','forfeit','founder','fraud','fraudulent','fumble','give','helpless','illiterate','illogical',
			'imperfect','impurity','inaccuracy','incompetence','incompetent','incurable','ineffective','ineffectiveness','ineffectual','inefficiency','injure','insane','insensible','insufficiency',
			'intoxicate','jobless','lag','lame','languish','lapse','lazily','leak','lose','lost','mess','mind','mishandle','mishap','misinform','misinformed','misrepresent','miss','mistaken',
			'mistrust','misunderstanding','misuse','neglect','nightmare','omit','order','oversight','perplexity','terrible','panned','stuck','stalled','unsure','disappointed','vanquished','bested']


hope = ['achievement','ambition','ambitious','anticipation','anticipate','aspiration','aspire','belief','believe','concern','confidence','confident','desire','expectation','expect','faith',
		'goal','optimism','optimistic','promise','prospect','prospective','wish','wishful','assumption','assume','buoyancy','daydream','dependence','endurance','endure','expectancy','fancy',
		'fortune','gain','hope','hopeful','hopefulness','reliance','reverie','reward','rosiness','sanguineness','utopia','bright side','castles in air',"fool's paradise",'greedy glutton',
		'light at end of tunnel','trust','virtue','despite','fulfill','future','believe','endure','bright','greener','positive','overcome']

disgust = ['abhorrence','abhor','abomination','antipathy','detestation','detest','dislike','distaste','hatefulness',
'hateful','hatred','loathing','loath','nausea','nauseation','nauseousness','objection','repugnance','revolt','revulsion',
'satiation','satiety','sickness','surfeit','sick','disfavor','disgust','repulsion','repulsive','repulse','odious']


religion = ['angel','angelic','believer','bible','biblical','bishop','bless','cathedral','catholic','chapel','christ',
'christian','christianity','christmas','church','clergyman','communion','congregation','congregational','crucifix',
'cult','devil','devotion','divine','divinity','easter','ecumenical','eternal','evangelism','ghost','god','goddess',
'gospel','grace','heaven','heavenly','hell','holy','hymn','magic','magical','metaphysical','metaphysics','miracle',
'miraculous','missionary','myth','orthodox','parish','pastor','piety','pilgrimage','pious','pope','pray','prayer',
'preach','preacher','priest','providence','rector','religion','religious','reverend','sacred','saint','salvation',
'seeker','seminary','sermon','sin','solemn','soul','spirit','spiritual','stoicism','supernatural','testament',
'theological','theology','whimsical','witch']

pain = ['ache', 'agonize', 'agony', 'ail', 'ailment', 'ambivalent', 'anguish', 'anxiety', 'anxious', 'anxiousness', 'apologetic', 'ashamed', 'beset', 
'bitter', 'bitterness', 'bloodshed', 'broken-hearted', 'brood', 'bruise', 'burdensome', 'chafe', 'clamor', 'clamorous', 'clatter', 'commiseration', 
'conflict', 'cramp', 'cringe', 'cripple', 'dejected', 'depress', 'depression', 'despair', 'desperate', 'desperation', 'despise', 'destitute', 
'disagreeable', 'disappoint', 'disappointment', 'discomfort', 'disconcerted', 'discontent', 'discourage', 'dishearten', 'dishonor', 
'disillusion', 'dismay', 'displeasure', 'dissatisfaction', 'dissatisfied', 'dissolution', 'distress', 'distrustful', 'doldrums', 'downcast', 
'downfall', 'downhearted', 'dread', 'estranged', 'exasperation', 'exhaustion', 'famine', 'fatigue', 'fearful', 'fearsome', 'forlorn', 
'frantic', 'frighten', 'frightful', 'frustrate', 'frustration', 'fury']

education = ['academic', 'academy', 'campus', 'chemistry', 'classroom', 
 'college', 'course', 'credit', 'dean', 'degree', 
'educate', 'educated', 'education', 'educational',  'english', 'essay', 'exam', 'examination', 'examine','examiner', 'experiment', 'faculty', 'form', 'freshman', 'geometry', 'grade', 'graduate', 
'graduation', 'grammar',  'institute', 'instruct', 'instruction', 
'instructor', 'intellect', 'intellectual', 'intelligence', 'junior', 'knowledge', 'lab', 'laboratory', 'learn', 
'learner', 'lecture', 'lesson', 'library', 'literalness', 'literary', 'literature', 'major', 'math', 
'school', 'mathematics', 'matriculate', 'museum',"kindergarten","teach","teacher","teachers" ]

legal = ['accuse', 'acquit', 'acquittal', 'advocate', 'allegation', 'amendment', 'amnesty', 'antitrust', 'appeal', 
'apply', 'arrest', 'attorney', 'auditor', 'authoritative', 'authority', 'authorize', 'autonomous', 'ax', 'bar', 'case', 'certificate', 'certification', 'certify', 'constable', 'convict', 'cop', 'counsel', 'court', 'crime', 'criminal', 'deposition', 'detective', 'discharge', 'disputable', 'divorce', 'enforce', 'enforcement', 'entitle', 'equity', 
'evict', 'evidence', 'excommunication', 'fugitive', 'guarantee', 'guilty', 'hearing', 'illegal', 'illegality', 
'imprison', 'imprisonment', 'impunity', 'indictment', 'infraction', 'infringement', 'injunction', 'innocent', 'jail', 
'judge', 'judgment', 'judicial', 'junta', 'jurisdiction', 'juror', 'jury', 'justice', 'kidnap', 'law', 'lawful', 
'lawless', 'lawyer', 'legal', 'legislation', 'legislative', 'legislator']

warfare = ['air', 'ambush', 'ammunition', 'arm', 'armed', 'armistice', 'army', 'arrow', 'battle', 'blockade', 'bomb', 
'bow', 'cannon', 'castle', 'cavalry', 'civil', 'club', 'colonel', 'commander', 'corporal', 'corps', 'coup', 'destroyer', 'discharge', 'draft', 'fight', 'fleet', 'force', 'fort', 'grenade', 'guard', 'guerrilla', 'gun', 'infantry', 
'intervention', 'legion', 'lieutenant', 'march', 'marcher', 'military', 'militia', 'minutemen', 'missile', 'munition', 'naval', 'navy', 'parachuter', 'parade', 'patrol', 'pentagon', 'pistol', 'private', 'radar', 'rebellion', 'recruit', 'regiment', 'retreat', 'rifle', 'rocket', 'sergeant', 'service', 'shell', 'soldier', 'spear', 'stronghold', 
'submarine', 'surrender', 'sword', 'tnt', 'trigger', 'troop', 'veteran', 'war', 'warfare', 'warrior', 'weapon']

politics = ['administration', 'adversary', 'alliance', 'allied', 'ally', 'ambassador', 'amendment', 'anarchist', 
'anarchy', 'antitrust', 'armistice', 'autocrat', 'autocratic', 'ballot', 'banish', 'banishment', 'bill', 'cabinet', 
'campaign', 'campaigner', 'candidate', 'capital', 'capitalism', 'capitol', 'census', 'chancellor', 'citizen', 'civil', 'coalition', 'colonial', 'colony', 'combat', 'commissioner', 'commonwealth', 'communism', 'communist', 'confederate', 'confederation', 'conference', 'congress', 'congressional', 'congressman', 'congressmen', 'conservatism', 
'conservative', 'conspiracy', 'constitution', 'constitutional', 'convention', 'corps', 'council', 'country', 'county', 'court', 'courtly', 'crown', 'crusade', 'crusader', 'debate', 'delegate', 'delegation', 'democracy', 'democrat', 
'democratic', 'demonstration', 'dictate', 'dictator', 'dictatorial', 'dictatorship', 'diplomacy', 'diplomatic', 
'discharge', 'draft', 'elect', 'election', 'elite', 'emancipation', 'embassy', 'emperor', 'empire', 'enslave', 
'entangle', 'entanglement', 'equality', 'establishment']

race = ['black', 'color', 'colored', 'desegregation', 'discrimination', 'ethnic', 'indian', 'jew', 'native', 'negro', 'nigger', 
'prejudice', 'race', 'racial', 'segregation', 'white','asian']


animals = ['animal', 'animals', 'ant', 'ants', 'badger', 'badgers', 'bat', 'bats', 'bear', 'bears', 'beaver', 'beavers', 'bird', 'birds', 'buffalo', 'buffaloes', 'bug', 'bugs', 'bull', 'bulls', 'buzzard', 'buzzards', 'camel', 'camels', 'cat', 'cats', 'cattle', 'chicken', 'cow', 'cows', 'coyote', 'coyotes', 'creature', 'creatures', 'deer', 'deer', 'dog', 'dogs', 'eagle', 'eagles', 'elephant', 'elephants', 'filly', 'fish', 'fly', 'fox', 'frog', 'frogs', 'goat', 'goats', 'hare', 'hen', 'herd', 'horse', 'horses', 'insect', 'insects', 'lion', 'lions', 'lioness', 'livestock', 
'mare', 'mice', 'monkey', 'monkeys', 'monster', 'monsters', 'moth', 'moths', 'mouse', 'mice', 'mule', 'mules', 'otter', 'otters', 'ox', 'oxen', 'peacock', 'peacocks', 'pet', 'pets', 'pig', 'pigs', 'pony', 'ponies', 'poultry', 'prey', 'puppy', 'puppies', 'rabbit', 'rabbits', 'rhinoceros', 'rodent', 'rodents', 'shark', 'sharks', 'sheep', 'sloth', 
'slug', 'snake', 'snakes', 'squirrel', 'squirrels', 'tiger', 'tigers', 'trout', 'trouts', 'turtle', 'turtles', 'viper', 'vipers', 'vulture', 'vultures', 'wolf', 'wolves']

food = ['bacon', 'bean', 'beef', 'beer', 'brandy', 'bread', 'breakfast', 'butter', 'cake', 'candy', 'cereal', 'cocktail', 'cocoa', 'coffee', 'cookie', 'cooky', 'corn', 'cream', 'crop', 'dinner', 'drink', 'drug', 'egg', 'feed', 'fig', 'food', 'fruit', 'gin', 'ginger', 'grain', 'grape', 'hamburger', 'hardtack', 'harvest', 'hay', 'heroin', 'ice', 'juice', 'lemon', 'lemonade', 'liquor', 'lunch', 'luncheon', 'meal', 'meat', 'milk', 'mutton', 'nourish', 'nourishment', 'nut', 'nutrient', 'oat', 'onion', 'pea', 'pie', 'produce', 'rice', 'salami', 'salt', 'snack', 'staple', 'steak', 'sugar', 'supper', 'sweet', 'syrup', 'tea', 'toast', 'tobacco', 'vegetable', 'vitamin', 'walnut', 'wheat', 'whisky', 'wine']

afghanistan  = ["afghanistan","afghan",'badakshan', 'badghis', 'baghlan', 'balkh', 'bamyan', 'daikundy', 'farah', 'faryab', 'ghazni', 'ghor', 'helmand', 'herat', 'kabul', 'kandahar', 'kapisa', 'khost', 'kunar', 'kunduz', 'laghman',
 'logar', 'nangarhar', 'nimroz', 'nuristan', 'paktya', 'panjshir', 'parwan', 'samangan', 'sar-e-pul', 'takhar', 'uruzgan', 'wardak', 'zabul', 'paktika', 'jawzjan',
 "hamid","karzai","kabul","ghani","ashraf","wolesi", "jirga"]



#Method 2
def filtertwo(filter1, filter2, articles):
	sublist = []
	filtered = []
	for article in articles:
		text = set(unicodedata.normalize('NFKD',article['text'].lower()).encode('ascii','ignore').split())
		score = len(text.intersection(filter1))
		sublist.append((score,article['title'],article))

	#sublist = list(set(sublist))
	sublist.sort()
	filtered_articles = []
	for i in range(50):
		filtered_articles.append(sublist[-i][2])

	count = 0
	for article in filtered_articles:
		text = set(unicodedata.normalize('NFKD',article['text'].lower()).encode('ascii','ignore').split())
		score = len(text.intersection(filter2))
		filtered.append((score,article['title']))

	filtered = list(set(filtered))
	filtered.sort()
	return filtered





def categorize_article(token_set,cat_tfidf_dict):
	category_score = 0.
	article_category_intersection = token_set.intersection(set(cat_tfidf_dict.keys()))
	if len(article_category_intersection) == 0:
		return 0.
	for token in article_category_intersection:
		category_score += cat_tfidf_dict[token]
	return category_score

def tfidf_filter(tokens,filter_words,idf_dict):
	cum_tfidf = 0.
	for token in set(tokens).intersection(set(filter_words)):
		tf = tokens.count(token) / float(len(tokens))
		if token not in idf_dict.keys():
			continue
		idf = idf_dict[token]
		cum_tfidf += tf * math.log(idf)
	return cum_tfidf / math.sqrt(len(tokens))

# with open("idf.pickled",'r') as f:
# 	idf_dict = dict(pickle.load(f))
# conn = Connection().newstune
# articles = conn.er_articles.find()
# filtered = []
# titles = set([])
# conn = Connection().newstune
# articles = conn.er_articles.find()
# #### Uncomment for Method 1
# for article in articles:
# 	if article['title'] in titles:
# 		continue
# 	titles.add(article['title'])
# 	tokens = tokenize_article(article['text'])
# 	cat_score = tfidf_filter(tokens, business, idf_dict)
# 	concept_score = tfidf_filter(tokens, partisan, idf_dict)
# 	article_len = len(tokens)
# 	filtered.append((cat_score,concept_score,article['title']))
	#token_set.intersection(set(business))


	#text = set(unicodedata.normalize('NFKD',article['text'].lower()).encode('ascii','ignore').split())
	#cat_score = categorize_article(token_set,cat_tfidf_dict) / math.sqrt(len(cat_tfidf_dict))
	#cat_score /= math.sqrt(article_len)
	#concept_score = len(token_set.intersection(set(partisan))) / math.sqrt(len(partisan))
	#concept_score /= math.sqrt(article_len)
	#if cat_score == 0 or concept_score == 0:
	#	continue
	#score = 1 + len(text.intersection([]))
	#score *= (1 + len(text.intersection(business)))
	#filtered.append((cat_score,concept_score,article['title']))
	#filtered.append(score,article['title'])

#filtered = list(set(filtered))
#normed = [(t[0] / math.sqrt(t[0]**2 + t[1]**2), t[1] / math.sqrt(t[0]**2 + t[1]**2),t[2]) for t in filtered if t[0] > 0 and t[1] > 0]
#mult = [(f[0] + f[1],f[0],f[1],f[2]) for f in normed]
# ceiling = [(f[0] + f[1],f[0],f[1],f[2]) for f in normed if < f[0] < ]
#filtered = filtertwo(partisan, religion, articles)
# filtered.sort()
# filtered2 = [(f[1],f[0],f[2]) for f in filtered[::-1][:100]]
# filtered2.sort()

# feed_urls = ["news/artsculture","reuters/businessNews","reuters/companyNews",
# 			 "reuters/entertainment","reuters/environment","reuters/healthNews",
# 			 "reuters/lifestyle","news/wealth", "reuters/oddlyEnoughNews",
# 			 "reuters/peopleNews", "Reuters/PoliticsNews", "reuters/scienceNews",
# 			 "reuters/sportsNews", "reuters/technologyNews","Reuters/domesticNews",
# 			 "Reuters/worldNews"]

#stemmer = SnowballStemmer("english")

#conn.er_articles.find({'date': {'$in': [ re.compile('2017[-]05[-]1')]}})

from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
conn = Connection().newstune
category = "reuters/businessNews"
articles = conn.er_articles.find({"category":category},{"text":1,"title":1})
#articles = conn.er_articles.find({"date":"2017-05-16"},{"text":1,"title":1})
articles = conn.er_articles.find({'date': {'$in': [ re.compile('2017[-]05[-]1')]}},{"text":1,"title":1})
filtered = []
titles = []
for article in articles:
	if article['title'] in titles:
		continue
	titles.append(article['title'])
	tokens = tokenize_article(article['text'])
	tokens = [lemmatizer.lemmatize(t) for t in tokens]
	article_len = len(tokens)
	s_filter = set([lemmatizer.lemmatize(t) for t in religion])
	filter2 = set([lemmatizer.lemmatize(t) for t in legal])
	#s_filter = set([stemmer.stem(t) for t in afghanistan])
	#filter2 = set([stemmer.stem(t) for t in education])
	score = float(len(set(tokens).intersection(s_filter))) / math.sqrt(article_len)
	score2 = float(len(set(tokens).intersection(filter2))) / math.sqrt(article_len)
	filtered.append((float(score) / math.sqrt(len(s_filter)),float(score2) / math.sqrt(len(filter2)),article['title']))
	#filtered.append((score,score2,article['title']))

filtered = list(set(filtered))
filtered.sort()
#for i in range(1,25): print filtered[-i][-1]



#find the pareto front and print
dominant = []
visited = []
for j in range(10):   
    Xs = [f[0] for f in filtered if f not in visited]
    Ys = [f[1] for f in filtered if f not in visited]
    p_frontX, p_frontY = pareto_frontier(Xs,Ys)
    for i in range(len(p_frontX)):
        for f in filtered:
            if f[0] == p_frontX[i] and f[1] == p_frontY[i] and f not in visited:
                median_score = f[0] * -1
                #median_score = 0
                if f[0] > 0.0 and f[1] > 0.0:
                    dominant.append((j,median_score,f[0],f[1],f[2]))
                visited.append(f)


dominant.sort()
for i in range(len(dominant)): print dominant[i][0],dominant[i][2],dominant[i][3],dominant[i][-1]

#gdelt #commoncrawlx

