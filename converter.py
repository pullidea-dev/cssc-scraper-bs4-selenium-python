import csv
import pandas as pd
from os import path
from resources import take_screenshot
from constants import SCREENSHOT_UPLOAD_URL, SLUG_FILTER_PATTERN
from datetime import datetime


filenameEmail = path.join(path.dirname(path.abspath(__file__)), 'csv', 'Rappers with Email updated.csv')
filenameCoupon = path.join(path.dirname(path.abspath(__file__)), 'csv', 'Coupon Codes.csv')
filenameFinal = path.join(path.dirname(path.abspath(__file__)), 'csv', 'Rappers with Email final.csv')

if not path.exists(filenameCoupon):
  print('Writing a new file for Coupon Code.')
  couponFile = open(filenameCoupon, 'w', newline='', encoding='utf-8-sig')
  couponwriter = csv.writer(couponFile, delimiter=',')
  couponwriter.writerow(['Edd Discount Name', 'Edd Discount Code', 'Edd Discount Amount', 'Edd Discount Type', 'Edd Discount Uses', 'Edd Discount Max Uses', 'Edd Discount Is Single Use', 'Edd Discount Start', 'Edd Discount Expiration', 'Edd Discount Status', 'Edd Discount Product Condition', 'Edd Discount Is Not Global', 'Edd Discount Min Price', 'Edd Discount Product Reqs', 'Title', 'URL Slug', 'Date', 'Modified Date', 'Status', 'Edd Discount Excluded Products', 'Post type'])
  couponFile.close()

if not path.exists(filenameFinal):
  print('Writing a new file for final csv.')
  finalFile = open(filenameFinal, 'w', newline='', encoding='utf-16')
  finalwriter = csv.writer(finalFile, delimiter='\t')
  finalwriter.writerow(['SoundCloudURL', 'UserName', 'FullName', 'ArtistName', 'ArtistNameCleaned', 'Location', 'Country', 'Email', 'InstagramUserName', 'InstagramURL', 'HasInstagram', 'SongTitle', 'SongTitleFull', 'GO+', 'SongLink', 'Genre', 'ArtistOrManager', 'NumberOfFollowers', 'Popularity', 'CouponCodeName', 'CouponCode', 'SongPlays', 'UploadDate', 'PopularityAdjusted', 'ActiveState', 'ScreenshotFileName', 'ScreenshotURL'])
  finalFile.close()

try:
  emaildf = pd.read_csv(filenameEmail, encoding='utf-8', header=0, error_bad_lines=False, sep=',')
except:
  emaildf = pd.read_csv(filenameEmail, encoding='utf-16', header=0, error_bad_lines=False, sep='\t')
  pass
coupondf = pd.read_csv(filenameCoupon, encoding='utf-8-sig', header=0, error_bad_lines=False, sep=',')

# print(list(emaildf.columns))

startdate = input('Start Date in the following format YYYY-MM-DD : ')
expiredate = input('Expiry Date in the following format YYYY-MM-DD : ')
dollaramount = input('Dollar Amount : ')

# print(emaildf['CouponCodeName'])

emaildf.drop_duplicates('CouponCodeName', inplace=True)
emaildf.reset_index(inplace=True)
newlines_all = emaildf[~emaildf['CouponCode'].isin(coupondf['Edd Discount Code'])].dropna(how = 'all')
newlines = pd.DataFrame(columns=['Edd Discount Name', 'Edd Discount Code', 'Edd Discount Amount', 'Edd Discount Type', 'Edd Discount Uses', 'Edd Discount Max Uses', 'Edd Discount Is Single Use', 'Edd Discount Start', 'Edd Discount Expiration', 'Edd Discount Status', 'Edd Discount Product Condition', 'Edd Discount Is Not Global', 'Edd Discount Min Price', 'Edd Discount Product Reqs', 'Title', 'URL Slug', 'Date', 'Modified Date', 'Status', 'Edd Discount Excluded Products', 'Post type'])
print('Data extracted from Email csv')



newlines['Edd Discount Name'] = newlines_all['ArtistNameCleaned'].apply(lambda x: f'Discount -${dollaramount} for mp3 lease for {x}')
newlines['Edd Discount Code'] = newlines_all['CouponCode']
newlines['Edd Discount Amount'] = dollaramount
newlines['Edd Discount Type'] = 'flat'
newlines['Edd Discount Uses'] = ''
newlines['Edd Discount Max Uses'] = 1
newlines['Edd Discount Is Single Use'] = ''
newlines['Edd Discount Start'] = startdate.strip() + ' 00:00'
newlines['Edd Discount Expiration'] = expiredate.strip() + ' 23:59'
newlines['Edd Discount Status'] = 'active'
newlines['Edd Discount Product Condition'] = 'all'
newlines['Edd Discount Is Not Global'] = ''
newlines['Edd Discount Min Price'] = ''
newlines['Edd Discount Product Reqs'] = ''
newlines['Title'] = newlines_all['Email']
newlines['URL Slug'] = newlines_all['UserName'].replace(' ', '_') + '_' + newlines_all['SongTitle'].apply(lambda x: x.split()[0].lower())
newlines['URL Slug'] = newlines['URL Slug'].apply(lambda x: SLUG_FILTER_PATTERN.sub('', x.lower()))
newlines['Date'] = datetime.now().strftime("%y-%m-%d %H:%M:%S")
newlines['Modified Date'] = datetime.now().strftime("%y-%m-%d %H:%M:%S")
newlines['Status'] = 'active'
newlines['Edd Discount Excluded Products'] = ''
newlines['Post type'] = 'edd_discount'

# newlines = newlines_all[['ArtistNameCleaned', 'CouponCode']].copy()
# newlines['ArtistNameCleaned'] = newlines['ArtistNameCleaned'].apply(lambda x: f'Discount -${dollaramount} for mp3 lease for {x}')
# newlines.rename(columns={'ArtistNameCleaned': 'CouponCodeName'}, inplace=True)
# newlines['DiscountAmount'] = dollaramount
# newlines['DiscountType'] = 'flat'
# newlines['Uses'] = '0'
# newlines['MaxUses'] = 1
# newlines['SingleUse'] = 0
# newlines['StartDate'] = startdate
# newlines['Expiration'] = expiredate
# newlines['DiscountStatus'] = 'active'
# newlines['ProductCondition'] = 'all'
# newlines['ProductRequirements'] = ''
# newlines['IsItOnlyForSelectProducts'] = '0'
# newlines['MinimumPurchasePrice'] = ''
print('{} new entries found.'.format(len(newlines.index)))
if len(newlines.index) > 0:
  print('The first entry is {}.'.format(newlines.iloc[0]['Title']))
  print('The last entry is {}.'.format(newlines.iloc[-1]['Title']))
print('New lines are ready to be appended. Now merging...')
newlines.to_csv(filenameCoupon, mode='a', header=False, encoding='utf-8', sep=',', index=False)
print('Merge finished and Coupon Codes.csv updated.')

if len(newlines.index) > 0:
  print('\nNow taking screenshots...')
  newlines_all['ScreenshotFileName'] = ''
  newlines_all['ScreenshotURL'] = ''
  newlines_all.drop('index', axis=1, inplace=True)

  for index, url in enumerate(newlines_all['SongLink']):
    filename = take_screenshot(url, newlines_all.iloc[index]['SoundCloudURL'].rsplit('/')[-1], newlines_all.iloc[index]['SongTitle'].rsplit()[0], newlines_all.iloc[index]['GO+'])
    if filename != 'None':
      newlines_all.iloc[index, newlines_all.columns.get_loc('ScreenshotFileName')] = filename
      newlines_all.iloc[index, newlines_all.columns.get_loc('ScreenshotURL')] = SCREENSHOT_UPLOAD_URL + filename
    else:
      newlines_all.iloc[index, newlines_all.columns.get_loc('ScreenshotFileName')] = 'N/A'
      newlines_all.iloc[index, newlines_all.columns.get_loc('ScreenshotURL')] = 'N/A'

  print('Moving to final csv')
  newlines_all.to_csv(filenameFinal, mode='a', header=False, encoding='utf-16', sep='\t', index=False)
