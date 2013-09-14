from rauth import OAuth2Session
import json
import urllib

client_id = '5217c86666cd9a423c000060'
client_secret = 'fd850e2070460f6e3bcb699fc2e30554'
access_token = '1/6beb5fbeba1e506db03e08c3439ec8cf'

BASE_URL = 'https://api.bufferapp.com/1/%s'

PATHS = {
  'info'				: 'info/configuration.json',
  "profiles" 			: "profiles.json",
  'updates_pending'		: "profiles/%s/updates/pending.json",
  'updates_create'		: "updates/create.json"
}

class API(object):
	def __init__(self, client_id, client_secret, access_token=None):
		self.session = OAuth2Session( client_id=client_id,
                                  client_secret=client_secret,
                                  access_token=access_token)

	@property
	def access_token(self):
		return self.session.access_token

	@access_token.setter
	def access_token(self, value):
		self.session.access_token = value

	def get(self, url, parser=None):
		if parser is None:
			parser = json.loads

		if not self.session.access_token:
			raise ValueError('Please set an access token first!')

		response = self.session.get(url=BASE_URL % url)

		return parser(response.content)

	def post(self, url, parser=None, **params):
		if parser is None:
			parser = json.loads

		if not self.session.access_token:
			raise ValueError('Please set an access token first!')

		headers = {'Content-Type':'application/x-www-form-urlencoded'}

		response = self.session.post(url=BASE_URL % url, headers=headers, **params)

		return parser(response.content)

	@property
	def info(self):
		return self.get(url=PATHS['info'])

	def profiles(self):
		return self.get(url=PATHS["profiles"])

	def updates_pending(self, profile_id):
		return self.get(url=PATHS["updates_pending"]%profile_id)

	def updates_create(self, **params):
		return self.post(PATHS["updates_create"], json.loads, **params)

api = API(client_id, client_secret, access_token)
profiles =  api.profiles()

cute_babies = None
for profile in profiles:
	if profile[u'service_username'] == 'Cute Babies':
		cute_babies = profile

profile_id = cute_babies["id"]

# print api.updates_create(data="text=%s&profile_ids[]=%s" % ("This is a test",profile_id))
# print api.updates_pending(profile_id)

imgs = ['shutterstock_100383059.jpg',
'shutterstock_100741480.jpg',
'shutterstock_101105392.jpg',
'shutterstock_102115531.jpg',
'shutterstock_102415606.jpg',
'shutterstock_103574327.jpg',
'shutterstock_105337910.jpg',
'shutterstock_105402920.jpg',
'shutterstock_106249760.jpg',
'shutterstock_109003526.jpg',
'shutterstock_109189967.jpg',
'shutterstock_110405771.jpg',
'shutterstock_110741879.jpg',
'shutterstock_110990129.jpg',
'shutterstock_111461498.jpg',
'shutterstock_112381181.jpg',
'shutterstock_112818493.jpg',
'shutterstock_113182546.jpg',
'shutterstock_114154828.jpg',
'shutterstock_114196099.jpg',
'shutterstock_114226522.jpg',
'shutterstock_114237985.jpg',
'shutterstock_115410961.jpg',
'shutterstock_115410973.jpg',
'shutterstock_115512421.jpg',
'shutterstock_115512430.jpg',
'shutterstock_115541389.jpg',
'shutterstock_115660021.jpg',
'shutterstock_116113150.jpg',
'shutterstock_116494750.jpg',
'shutterstock_116494774.jpg',
'shutterstock_117378508.jpg',
'shutterstock_117589528.jpg',
'shutterstock_118550275.jpg',
'shutterstock_119165239.jpg',
'shutterstock_119918356.jpg',
'shutterstock_120651157.jpg',
'shutterstock_120766024.jpg',
'shutterstock_121099621.jpg',
'shutterstock_121477342.jpg',
'shutterstock_121655068.jpg',
'shutterstock_122383189.jpg',
'shutterstock_122598697.jpg',
'shutterstock_122985370.jpg',
'shutterstock_124529878.jpg',
'shutterstock_124881403.jpg',
'shutterstock_126210218.jpg',
'shutterstock_127899839.jpg',
'shutterstock_127975448.jpg',
'shutterstock_128463791.jpg',
'shutterstock_128679134.jpg',
'shutterstock_128859898.jpg',
'shutterstock_129268223.jpg',
'shutterstock_129342935.jpg',
'shutterstock_129792116.jpg',
'shutterstock_130471265.jpg',
'shutterstock_130746401.jpg',
'shutterstock_131269463.jpg',
'shutterstock_131606186.jpg',
'shutterstock_131609198.jpg',
'shutterstock_131878202.jpg',
'shutterstock_132040286.jpg',
'shutterstock_132874577.jpg',
'shutterstock_135379454.jpg',
'shutterstock_137903813.jpg',
'shutterstock_138225722.jpg',
'shutterstock_151737704.jpg',
'shutterstock_16433998.jpg',
'shutterstock_20054365.jpg',
'shutterstock_46734763.jpg',
'shutterstock_66721291.jpg',
'shutterstock_69251446.jpg',
'shutterstock_71001646.jpg',
'shutterstock_72370393.jpg',
'shutterstock_73835482.jpg',
'shutterstock_74124883.jpg',
'shutterstock_74689858.jpg',
'shutterstock_77732575.jpg',
'shutterstock_79429345.jpg',
'shutterstock_82237597.jpg',
'shutterstock_83131060.jpg',
'shutterstock_83470978.jpg',
'shutterstock_84000409.jpg',
'shutterstock_84324943.jpg',
'shutterstock_85462084.jpg',
'shutterstock_85536208.jpg',
'shutterstock_86152309.jpg',
'shutterstock_86350150.jpg',
'shutterstock_87729895.jpg',
'shutterstock_89744182.jpg',
'shutterstock_90112666.jpg',
'shutterstock_90809123.jpg',
'shutterstock_90889808.jpg',
'shutterstock_91075361.jpg',
'shutterstock_91191974.jpg',
'shutterstock_94584643.jpg',
'shutterstock_94905691.jpg',
'shutterstock_96618217.jpg',
'shutterstock_98034125.jpg',
'shutterstock_98870129.jpg',
'shutterstock_99322658.jpg',
'shutterstock_99544907.jpg']

for img in imgs:
    print api.updates_create(data="text=%s&profile_ids[]=%s&media[picture]=%s&media[thumbnail]=%s" % ("aaa",profile_id, urllib.quote_plus("http://s3.amazonaws.com/cutebabyco/%s" % img), urllib.quote_plus("http://s3.amazonaws.com/cutebabyco/%s" % img)))