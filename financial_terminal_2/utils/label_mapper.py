import Levenshtein as lev
import re
from collections import defaultdict


class LabelMapper:

    def __init__(self, data: dict):
        self.data = data
        self.labels = self.get_labels()
        print(self.labels)
        
        self.fundamentals_keys = {
            'income_statement': ["TaxEffectOfUnusualItems", "TaxRateForCalcs", "NormalizedEBITDA", "NormalizedDilutedEPS",
                        "NormalizedBasicEPS", "TotalUnusualItems", "TotalUnusualItemsExcludingGoodwill",
                        "NetIncomeFromContinuingOperationNetMinorityInterest", "ReconciledDepreciation",
                        "ReconciledCostOfRevenue", "EBITDA", "EBIT", "NetInterestIncome", "InterestExpense",
                        "InterestIncome", "ContinuingAndDiscontinuedDilutedEPS", "ContinuingAndDiscontinuedBasicEPS",
                        "NormalizedIncome", "NetIncomeFromContinuingAndDiscontinuedOperation", "TotalExpenses",
                        "RentExpenseSupplemental", "ReportedNormalizedDilutedEPS", "ReportedNormalizedBasicEPS",
                        "TotalOperatingIncomeAsReported", "DividendPerShare", "DilutedAverageShares", "BasicAverageShares",
                        "DilutedEPS", "DilutedEPSOtherGainsLosses", "TaxLossCarryforwardDilutedEPS",
                        "DilutedAccountingChange", "DilutedExtraordinary", "DilutedDiscontinuousOperations",
                        "DilutedContinuousOperations", "BasicEPS", "BasicEPSOtherGainsLosses", "TaxLossCarryforwardBasicEPS",
                        "BasicAccountingChange", "BasicExtraordinary", "BasicDiscontinuousOperations",
                        "BasicContinuousOperations", "DilutedNIAvailtoComStockholders", "AverageDilutionEarnings",
                        "NetIncomeCommonStockholders", "OtherunderPreferredStockDividend", "PreferredStockDividends",
                        "NetIncome", "MinorityInterests", "NetIncomeIncludingNoncontrollingInterests",
                        "NetIncomeFromTaxLossCarryforward", "NetIncomeExtraordinary", "NetIncomeDiscontinuousOperations",
                        "NetIncomeContinuousOperations", "EarningsFromEquityInterestNetOfTax", "TaxProvision",
                        "PretaxIncome", "OtherIncomeExpense", "OtherNonOperatingIncomeExpenses", "SpecialIncomeCharges",
                        "GainOnSaleOfPPE", "GainOnSaleOfBusiness", "OtherSpecialCharges", "WriteOff",
                        "ImpairmentOfCapitalAssets", "RestructuringAndMergernAcquisition", "SecuritiesAmortization",
                        "EarningsFromEquityInterest", "GainOnSaleOfSecurity", "NetNonOperatingInterestIncomeExpense",
                        "TotalOtherFinanceCost", "InterestExpenseNonOperating", "InterestIncomeNonOperating",
                        "OperatingIncome", "OperatingExpense", "OtherOperatingExpenses", "OtherTaxes",
                        "ProvisionForDoubtfulAccounts", "DepreciationAmortizationDepletionIncomeStatement",
                        "DepletionIncomeStatement", "DepreciationAndAmortizationInIncomeStatement", "Amortization",
                        "AmortizationOfIntangiblesIncomeStatement", "DepreciationIncomeStatement", "ResearchAndDevelopment",
                        "SellingGeneralAndAdministration", "SellingAndMarketingExpense", "GeneralAndAdministrativeExpense",
                        "OtherGandA", "InsuranceAndClaims", "RentAndLandingFees", "SalariesAndWages", "GrossProfit",
                        "CostOfRevenue", "TotalRevenue", "ExciseTaxes", "OperatingRevenue", "LossAdjustmentExpense",
                        "NetPolicyholderBenefitsAndClaims", "PolicyholderBenefitsGross", "PolicyholderBenefitsCeded",
                        "OccupancyAndEquipment", "ProfessionalExpenseAndContractServicesExpense", "OtherNonInterestExpense"],
            'balance_sheet': ["TreasurySharesNumber", "PreferredSharesNumber", "OrdinarySharesNumber", "ShareIssued", "NetDebt",
                            "TotalDebt", "TangibleBookValue", "InvestedCapital", "WorkingCapital", "NetTangibleAssets",
                            "CapitalLeaseObligations", "CommonStockEquity", "PreferredStockEquity", "TotalCapitalization",
                            "TotalEquityGrossMinorityInterest", "MinorityInterest", "StockholdersEquity",
                            "OtherEquityInterest", "GainsLossesNotAffectingRetainedEarnings", "OtherEquityAdjustments",
                            "FixedAssetsRevaluationReserve", "ForeignCurrencyTranslationAdjustments",
                            "MinimumPensionLiabilities", "UnrealizedGainLoss", "TreasuryStock", "RetainedEarnings",
                            "AdditionalPaidInCapital", "CapitalStock", "OtherCapitalStock", "CommonStock", "PreferredStock",
                            "TotalPartnershipCapital", "GeneralPartnershipCapital", "LimitedPartnershipCapital",
                            "TotalLiabilitiesNetMinorityInterest", "TotalNonCurrentLiabilitiesNetMinorityInterest",
                            "OtherNonCurrentLiabilities", "LiabilitiesHeldforSaleNonCurrent", "RestrictedCommonStock",
                            "PreferredSecuritiesOutsideStockEquity", "DerivativeProductLiabilities", "EmployeeBenefits",
                            "NonCurrentPensionAndOtherPostretirementBenefitPlans", "NonCurrentAccruedExpenses",
                            "DuetoRelatedPartiesNonCurrent", "TradeandOtherPayablesNonCurrent",
                            "NonCurrentDeferredLiabilities", "NonCurrentDeferredRevenue",
                            "NonCurrentDeferredTaxesLiabilities", "LongTermDebtAndCapitalLeaseObligation",
                            "LongTermCapitalLeaseObligation", "LongTermDebt", "LongTermProvisions", "CurrentLiabilities",
                            "OtherCurrentLiabilities", "CurrentDeferredLiabilities", "CurrentDeferredRevenue",
                            "CurrentDeferredTaxesLiabilities", "CurrentDebtAndCapitalLeaseObligation",
                            "CurrentCapitalLeaseObligation", "CurrentDebt", "OtherCurrentBorrowings", "LineOfCredit",
                            "CommercialPaper", "CurrentNotesPayable", "PensionandOtherPostRetirementBenefitPlansCurrent",
                            "CurrentProvisions", "PayablesAndAccruedExpenses", "CurrentAccruedExpenses", "InterestPayable",
                            "Payables", "OtherPayable", "DuetoRelatedPartiesCurrent", "DividendsPayable", "TotalTaxPayable",
                            "IncomeTaxPayable", "AccountsPayable", "TotalAssets", "TotalNonCurrentAssets",
                            "OtherNonCurrentAssets", "DefinedPensionBenefit", "NonCurrentPrepaidAssets",
                            "NonCurrentDeferredAssets", "NonCurrentDeferredTaxesAssets", "DuefromRelatedPartiesNonCurrent",
                            "NonCurrentNoteReceivables", "NonCurrentAccountsReceivable", "FinancialAssets",
                            "InvestmentsAndAdvances", "OtherInvestments", "InvestmentinFinancialAssets",
                            "HeldToMaturitySecurities", "AvailableForSaleSecurities",
                            "FinancialAssetsDesignatedasFairValueThroughProfitorLossTotal", "TradingSecurities",
                            "LongTermEquityInvestment", "InvestmentsinJointVenturesatCost",
                            "InvestmentsInOtherVenturesUnderEquityMethod", "InvestmentsinAssociatesatCost",
                            "InvestmentsinSubsidiariesatCost", "InvestmentProperties", "GoodwillAndOtherIntangibleAssets",
                            "OtherIntangibleAssets", "Goodwill", "NetPPE", "AccumulatedDepreciation", "GrossPPE", "Leases",
                            "ConstructionInProgress", "OtherProperties", "MachineryFurnitureEquipment",
                            "BuildingsAndImprovements", "LandAndImprovements", "Properties", "CurrentAssets",
                            "OtherCurrentAssets", "HedgingAssetsCurrent", "AssetsHeldForSaleCurrent", "CurrentDeferredAssets",
                            "CurrentDeferredTaxesAssets", "RestrictedCash", "PrepaidAssets", "Inventory",
                            "InventoriesAdjustmentsAllowances", "OtherInventories", "FinishedGoods", "WorkInProcess",
                            "RawMaterials", "Receivables", "ReceivablesAdjustmentsAllowances", "OtherReceivables",
                            "DuefromRelatedPartiesCurrent", "TaxesReceivable", "AccruedInterestReceivable", "NotesReceivable",
                            "LoansReceivable", "AccountsReceivable", "AllowanceForDoubtfulAccountsReceivable",
                            "GrossAccountsReceivable", "CashCashEquivalentsAndShortTermInvestments",
                            "OtherShortTermInvestments", "CashAndCashEquivalents", "CashEquivalents", "CashFinancial",
                            "CashCashEquivalentsAndFederalFundsSold"],
            'cash_flow': ["ForeignSales", "DomesticSales", "AdjustedGeographySegmentData", "FreeCashFlow",
                        "RepurchaseOfCapitalStock", "RepaymentOfDebt", "IssuanceOfDebt", "IssuanceOfCapitalStock",
                        "CapitalExpenditure", "InterestPaidSupplementalData", "IncomeTaxPaidSupplementalData",
                        "EndCashPosition", "OtherCashAdjustmentOutsideChangeinCash", "BeginningCashPosition",
                        "EffectOfExchangeRateChanges", "ChangesInCash", "OtherCashAdjustmentInsideChangeinCash",
                        "CashFlowFromDiscontinuedOperation", "FinancingCashFlow", "CashFromDiscontinuedFinancingActivities",
                        "CashFlowFromContinuingFinancingActivities", "NetOtherFinancingCharges", "InterestPaidCFF",
                        "ProceedsFromStockOptionExercised", "CashDividendsPaid", "PreferredStockDividendPaid",
                        "CommonStockDividendPaid", "NetPreferredStockIssuance", "PreferredStockPayments",
                        "PreferredStockIssuance", "NetCommonStockIssuance", "CommonStockPayments", "CommonStockIssuance",
                        "NetIssuancePaymentsOfDebt", "NetShortTermDebtIssuance", "ShortTermDebtPayments",
                        "ShortTermDebtIssuance", "NetLongTermDebtIssuance", "LongTermDebtPayments", "LongTermDebtIssuance",
                        "InvestingCashFlow", "CashFromDiscontinuedInvestingActivities",
                        "CashFlowFromContinuingInvestingActivities", "NetOtherInvestingChanges", "InterestReceivedCFI",
                        "DividendsReceivedCFI", "NetInvestmentPurchaseAndSale", "SaleOfInvestment", "PurchaseOfInvestment",
                        "NetInvestmentPropertiesPurchaseAndSale", "SaleOfInvestmentProperties",
                        "PurchaseOfInvestmentProperties", "NetBusinessPurchaseAndSale", "SaleOfBusiness",
                        "PurchaseOfBusiness", "NetIntangiblesPurchaseAndSale", "SaleOfIntangibles", "PurchaseOfIntangibles",
                        "NetPPEPurchaseAndSale", "SaleOfPPE", "PurchaseOfPPE", "CapitalExpenditureReported",
                        "OperatingCashFlow", "CashFromDiscontinuedOperatingActivities",
                        "CashFlowFromContinuingOperatingActivities", "TaxesRefundPaid", "InterestReceivedCFO",
                        "InterestPaidCFO", "DividendReceivedCFO", "DividendPaidCFO", "ChangeInWorkingCapital",
                        "ChangeInOtherWorkingCapital", "ChangeInOtherCurrentLiabilities", "ChangeInOtherCurrentAssets",
                        "ChangeInPayablesAndAccruedExpense", "ChangeInAccruedExpense", "ChangeInInterestPayable",
                        "ChangeInPayable", "ChangeInDividendPayable", "ChangeInAccountPayable", "ChangeInTaxPayable",
                        "ChangeInIncomeTaxPayable", "ChangeInPrepaidAssets", "ChangeInInventory", "ChangeInReceivables",
                        "ChangesInAccountReceivables", "OtherNonCashItems", "ExcessTaxBenefitFromStockBasedCompensation",
                        "StockBasedCompensation", "UnrealizedGainLossOnInvestmentSecurities", "ProvisionandWriteOffofAssets",
                        "AssetImpairmentCharge", "AmortizationOfSecurities", "DeferredTax", "DeferredIncomeTax",
                        "DepreciationAmortizationDepletion", "Depletion", "DepreciationAndAmortization",
                        "AmortizationCashFlow", "AmortizationOfIntangibles", "Depreciation", "OperatingGainsLosses",
                        "PensionAndEmployeeBenefitExpense", "EarningsLossesFromEquityInvestments",
                        "GainLossOnInvestmentSecurities", "NetForeignCurrencyExchangeGainLoss", "GainLossOnSaleOfPPE",
                        "GainLossOnSaleOfBusiness", "NetIncomeFromContinuingOperations",
                        "CashFlowsfromusedinOperatingActivitiesDirect", "TaxesRefundPaidDirect", "InterestReceivedDirect",
                        "InterestPaidDirect", "DividendsReceivedDirect", "DividendsPaidDirect", "ClassesofCashPayments",
                        "OtherCashPaymentsfromOperatingActivities", "PaymentsonBehalfofEmployees",
                        "PaymentstoSuppliersforGoodsandServices", "ClassesofCashReceiptsfromOperatingActivities",
                        "OtherCashReceiptsfromOperatingActivities", "ReceiptsfromGovernmentGrants", "ReceiptsfromCustomers"]
            }
  
        
        self.label_mapper = self.make_label_mapper()


    def compare_labels(self, label1: str, label2: str) -> int:
        distance = lev.distance(label1, label2)
        # print(f'Distance between {label1} and {label2}: {distance}')
        return distance


    def get_labels(self) -> list:
        """Gets all metric labels from the data."""
        return [label for label in self.data.get('facts').get('us-gaap').keys()]


    def match_metric(self, standard_label: str) -> str:
        """Returns the metric label that is closest to the standard label."""
        return min(self.labels, key=lambda label: self.compare_labels(standard_label, label), default=None)


    def make_label_mapper(self) -> dict:
        mapper = defaultdict(dict)

        for statement, standard_labels in self.fundamentals_keys.items():
            for standard_label in standard_labels:
                matched_label = self.match_metric(standard_label)
            
                mapper[statement][standard_label] = matched_label
            
        return mapper
