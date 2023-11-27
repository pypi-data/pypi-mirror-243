class MappingTable:

    @staticmethod
    def get_kline_map():
        return {'HTSCSecurityID': 'htsc_code', 'OpenPx': 'open', 'ClosePx': 'close', 'HighPx': 'high', 'LowPx': 'low',
                'NumTrades': 'num_trades', 'TotalVolumeTrade': 'volume', 'TotalValueTrade': 'value',
                'OpenInterest': 'open_interest', 'SettlePrice': 'settle'}

    @staticmethod
    def get_htsc_margin_map():
        return {'HTSCSecurityID': 'htsc_code', 'TradingPhaseCode': 'trading_phase', 'securityIDSource': 'exchange',
                'securityType': 'security_type', 'PreWeightedRate': 'pre_weighted_rate', 'PreHighRate': 'pre_high_rate',
                'PreLowRate': 'pre_low_rate', 'PreHtscVolume': 'pre_htsc_volume',
                'PreMarketVolume': 'pre_market_volume', 'WeightedRate': 'weighted_rate', 'HighRate': 'high_rate',
                'LowRate': 'low_rate', 'HtscVolume': 'htsc_volume', 'MarketVolume': 'market_volume',
                'BestBorrowRate': 'best_borrow_rate', 'BestLendRate': 'best_lend_rate', 'ValidBorrows': 'valid_borrows',
                'ValidALends': 'valid_a_lends', 'ValidBLends': 'valid_b_lends', 'ValidCLends': 'valid_c_lends',
                'ALends': 'a_lends', 'BLends': 'b_lends', 'CLends': 'c_lends',
                'ValidReservationBorrows': 'valid_reservation_borrows',
                'ValidReservationLends': 'valid_reservation_lends', 'ReservationBorrows': 'reservation_borrows',
                'ReservationLends': 'reservation_lends', 'ValidOtcLends': 'valid_otc_lends',
                'BestReservationBorrowRate': 'best_reservationborrow_rate',
                'BestReservationLendRate': 'best_reservation_lend_rate', 'ValidLendAmount': 'valid_lend_amount',
                'ValidALendAmount': 'valid_a_lend_amount', 'ValidBLendAmount': 'valid_b_lend_amount',
                'HtscBorrowAmount': 'htsc_borrow_amount', 'HtscBorrowRate': 'htsc_borrow_rate',
                'BestLoanRate': 'best_loan_rate', 'HtscBorrowTradeVolume': 'htsc_borrow_trade_volume',
                'HtscBorrowWeightedRate': 'htsc_borrow_weighted_rate',
                'PreHtscBorrowTradeVolume': 'pre_htsc_borrow_trade_volume',
                'PreHtscBorrowWeightedRate': 'pre_htsc_borrow_weighted_rate', 'HtscBorrows': 'htsc_borrows',
                'Loans': 'loans', 'ExternalLends': 'external_lends', 'LongTermLends': 'long_term_lends',
                'LastPx': 'last', 'PreClosePx': 'pre_close', 'Borrows': 'borrows',
                'HtscLendTradeVolume': 'htsc_lend_trade_volume', 'MarketTradeVolume': 'market_trade_volume',
                'TradeDate': 'trade_date', 'HtscLendAmount': 'htsc_lend_amount', 'HtscLendTerms': 'htsc_lend_terms',
                'HtscBestLendRate': 'htsc_best_lend_rate', 'HtscBorrowTerms': 'htsc_borrow_terms',
                'TradeVolume': 'trade_volume', 'TradeMoney': 'trade_money', 'PreTradeVolume': 'pre_trade_volume',
                'PreTradeMoney': 'pre_trade_money', }

    @staticmethod
    def get_derived_map():
        return {'HTSCSecurityID': 'htsc_code', 'securityIDSource': 'exchange', 'securityType': 'security_type',
                'TotalValueTrade': 'value', 'TotalBidValueTrade': 'total_buy_value_trade',
                'TotalOfferValueTrade': 'total_sell_value_trade', }

    @staticmethod
    def find_edb_index_map():
        return {'ModifyFrequency': 'modify_frequency', 'IndexId': 'index_id', 'Unit': 'unit',
                 'IndexCodeSource': 'index_code_source', 'PathSource': 'path_source', 'IndustryCode': 'industry_code',
                 'AccessId': 'access_id', 'IndexName': 'name', 'AccessName': 'access_name',
                 'ResourceId': 'resource_id', 'IndexStatus': 'index_status', 'Refenence3': 'refenence3',
                 'IS_COMPLIANCE': 'is_compliance'}

    @staticmethod
    def edb_map():
        return {'IndexValue': 'index_value', 'IndexId': 'index_id', 'AccessId': 'access_id', 'PubDate': 'pub_date',
                 'AccessName': 'access_name'}

    @classmethod
    def perform_operation(cls, method_name):
        method = getattr(cls, method_name)
        return method()


if __name__ == '__main__':
    n = MappingTable.perform_operation("get_kline_map")
    print(n)
