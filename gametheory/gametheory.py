import sys
sys.path.append('../')

import simulator.simulator as sim

DEFAULT_FLOOR = 0.1 / 1000

class GameTheory(sim.Simulator):
    """
    Currently uses an *approximate* running average that doesn't require
    tracking past elements.
    """

    def __init__(self, window, weight, start=(11, 0), stop=(15, 23), **kwargs):
        Simulator.__init__(self, start, stop, limit, download, delete)
        self.window = window
        self.weight = weight
        self.lowAvg = 0.0
        self.highAvg = 0.0

    def calculate_price_floor(self, input_features):
        return self.lowAvg * self.weight + self.highAvg * (1 - self.weight)

    def process_line(self, line, input_features, bids):
        if len(bids) < 2:
            return
        self.lowAvg = self.lowAvg * (self.window - 1)/self.window +\
                bids[1] * 1.0/self.window
        self.highAvg = self.highAvg * (self.window - 1)/self.window +\
                bids[1] * 1.0/self.window

class GameTheoryPerID(sim.Simulator):
    """
    Currently uses a running average that doesn't require tracking past 
    elements.
    Reserve is the greatest recorded average among ids from bid_requests, 
    multiplied by a weight parameter. *NOTE* weight parameter doesn't function
    in the same way as the weight parameter from GameTheory().
    """

    def __init__(self, window, weight, start=(11, 0), stop=(15, 23), **kwargs):
        Simulator.__init__(self, start, stop, **kwargs)
        self.window = window
        self.weight = weight
        self.input = "bid_requests"
        self.output = "campaign_id"
        self.averages = {}
        self.counts = {}

    def calculate_price_floor(self, input_features):
        keys = input_features[self.input]
        seenIDs = [k for k in keys if (k in self.averages)]
        if len(seenIDs) == 0:
            return DEFAULT_FLOOR
        else: 
            return max([self.averages[key] for key in seenIDs]) * self.weight

    def process_line(self, line, input_features, bids):
        bidResponses = line["bid_responses"]
        for response in bidResponses:
            bidderID = response["id"]
            price = response["bid_price"] 
            if bidderID in self.averages:
                n = min(self.counts[bidderID] + 1, self.window)
                self.averages[bidderID] = self.averages[bidderID] * (n - 1)/n +\
                        price * 1.0/n
                self.counts[bidderID] += 1
            else:
                self.averages[bidderID] = price
                self.counts[bidderID] = 1



# {"geo_timezone": "America/Indianapolis", "pub_network_id": 267, "site_id":
# 3878, "campaign_id": 3389, "ua_device": "iPhone", "geo_region_name": "IN",
# "i_txn_fee": 0.0, "r_timestamp": "2018-02-11T00:00:00.420682Z",
# "ua_device_type": "MOB", "r_num_ads_third_party": 0, "campaign_type": "rtb",
# "vv_cnt": 0, "r_cnt": 1, "ad_network_id": 408, "bid_requests": [5479, 18887,
# 9289, 21037, 12077, 9968, 22130, 2547, 21493, 1013, 21494, 12055, 15127, 2523,
# 3389, 22557, 7486], "cr_cnt": 1, "f_cnt": 0, "i_cnt": 1, "exp_mode": "20",
# "i_timestamp": "2018-02-11T00:00:01.287000Z", "rate_metric": "CPM", "ua_name":
# "Facebook", "c_cnt": 0, "ad_type": ["story"], "advertiser_id": 1021, "txn_fee":
# 0.0, "txn_rate": 0.000178498, "bid_responses": [{"buyer_seat_id": "acc-497",
# "bid_price": 0.000168498, "id": 2547}, {"buyer_seat_id": "27911", "bid_price":
# 7.87575874e-05, "id": 1013}, {"buyer_seat_id": "250", "bid_price": 0.0002748,
# "id": 3389}], "geo_continent_code": "NA", "ua_os_name": "iOS", "vi_cnt": 0,
# "r_num_ads_returned": 1, "zone_id": 5745, "i_txn_rate": 0.000178498,
# "session_id": "2c1425441a6a49dc9999663bd48cfff2_a33c8f55", "token":
# "rtb:11:250_10000", "r_num_ads_requested": 1, "geo_dma_code": 527,
# "geo_country_code2": "US", "creative_id": 56440, "ua_os": "iOS 10.3",
# "geo_city_name": "Greencastle", "geo_area_code": 765} 
