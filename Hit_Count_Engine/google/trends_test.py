# https://github.com/GeneralMills/pytrends
from pytrends.request import TrendReq

pytrend_all = TrendReq()
# pytrend_normal = TrendReq()
# pytrend_compsec = TrendReq()

# https://github.com/pat310/google-trends-api/wiki/Google-Trends-Categories
# category 314 is computer security
#            0 is all
#            7 is finance
#          697 is footwear
#          303 is operating systems
# timeframe 'today #-m' == from last # months, # can be 1, 3, 12 months

# pytrend_all.build_payload(kw_list=["puma", "nike", "adidas"], cat="697", timeframe="now 1-H")
pytrend_all.build_payload(kw_list=["apple", "windows", "linux"], cat="303", timeframe="today 3-m")
# pytrend_normal.outputbuild_payload(kw_list=["volatility"], cat="314", timeframe="today 12-m")

int_all_df = pytrend_all.interest_over_time()
# int_normal_df = pytrend_normal.interest_over_time()
# int_compsec_df = pytrend_compsec.interest_over_time()

# joined = (
# int_all_df.loc[:, ["volatility"]]
# .join(int_normal_df.loc[:, ["volatility"]], lsuffix="_all", rsuffix="_normal")
# .join(int_compsec_df.loc[:, ["volatility"]], rsuffix="compsec")
# )

# print(joined)
print(int_all_df)
summa = int_all_df.sum(numeric_only=True) / len(int_all_df)  # TODO: calculate average (values between 0 and 100)
print(summa)
print(summa.idxmax())


"""
plt.plot(int_all_df.iloc[:,0],int_all_df.iloc[:,1], label = "apple")
plt.plot(int_all_df.iloc[:,0],int_all_df.iloc[:,2], label = "windows")
plt.plot(int_all_df.iloc[:,0],int_all_df.iloc[:,3], label = "linux")
plt.legend(loc="upper left")
"""
