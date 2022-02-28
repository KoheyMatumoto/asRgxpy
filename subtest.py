
import shutil
import re
import os
from time import sleep
import pandas as pd
import numpy as np
import html

from adv_class_scripts import UI_ins
from adv_class_scripts import SELENIUM_ins
from adv_class_scripts import functions
from adv_class_scripts import GSPREAD_ins
from adv_class_scripts import AUTOGUI_ins
from adv_class_scripts import DATAFRAME_PD_ins



import re

st = '''<h3>【プラン別】解約手数料が発生するのはいつ？</h3>
<img src="https://mizu-cool.jp/wp-content/uploads/2021/01/a5c6a7e2f0ea6811b0057f1d77b686d8.jpg" alt="解約手数料が発生する期間" width="700" height="350" class="aligncenter size-full wp-image-3385" />
<p>ウォーターワンでは、2つのプラン<span class="huto">「①基本プラン」</span>と<span class="huto">「②3年うきうきパック」</span>があります。</p>
<p>それぞれのプランごとに<span class="bmarker">契約期間と解約手数料</span>を見てみましょう。</p>

<div class="st-centertable">
<table>
	<tbody>
		<tr>
			<td bgcolor="#c2ecf9" width="30%"></td>
			<td bgcolor="#c2ecf9" width="35%"><span class="huto">契約期間</span></td>
			<td bgcolor="#c2ecf9" width="35%"><span class="huto">解約手数料</span></td>
		</tr>
'''
ptn = '<td.*?>(.+?)<\/td>'
#正規表現で（）を$1で置きたいやつ、pyのre subでは\\1とすることで置くことができる
st = re.sub(ptn,'<th class="okikae">\\1</th>',st)
print(st)