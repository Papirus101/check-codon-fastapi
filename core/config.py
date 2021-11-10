from starlette.config import Config

config = Config('.env')

DATABASE_URL = config('FA_DATABASE_URL', cast=str, default='')
ACCESS_TOKEN_EXPIRE = 60
ALGORITHM = 'HS256'
SECRET_KEY = config('FA_SECRET_KEY', cast=str, default='47bd229e19354fa2898906fa97f56ce8f5f928bd091b5f8c563990f86057226e')
DNK = '''tgacccactaatcagcaacatagcactttgagcaaaggcctgtgttggagctattggccc
         caaaactgcctttccctaaacagtgttcaccattgtagacctcaccactgttcgcgtaac
         aactggcatgtcctgggggttaatactcac
      '''