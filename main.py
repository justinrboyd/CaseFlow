from dataclasses import dataclass
from datetime import date, datetime, timedelta
from bisect import bisect_right
from typing import Optional


@dataclass(frozen = True)
class RateRow:
    effective_date: date        # compare/sort safely as date
    annual_rate_percent: float  # e.g., 8.0 for 8%
    daily_rate_decimal: float   # e.g., 0.08 / 365 for daily rate

class RateDatabase:
    def __init__(self):
        # series_id -> sorted list of RateRow by effective_date
        self.rate_series: dict[str, list[RateRow]] = {}

    def add_rate(self, series_id: str, rate_row: RateRow) -> None:
        series = self.rate_series.setdefault(series_id, [])

        # Enforce ascending order and no duplicates
        if series:
            last = series[-1].effective_date
            if rate_row.effective_date <= last:
                raise ValueError(
                    f"Rate effective date {rate_row.effective_date} "
                    f"must be after last date {last} in series {series_id}"
                )
        
        series.append(rate_row)

    def get_rate_as_of(self, series_id: str, as_of: date | datetime) -> Optional[RateRow]:
        series = self.rate_series.get(series_id)
        if not series:
            return None
        
        if isinstance(as_of, datetime):
            as_of = as_of.date()

        dates = [r.effective_date for r in series]
        i = bisect_right(dates, as_of) - 1
        if i < 0:
            return None
        return series[i]


class App:
    def __init__(self):
        self.db = RateDatabase()

        # Florida Post-Judgment Interest Rates 
        series_id = "FL_POST_JUDGMENT"

        ### Rate Table Data 
        ### Table entries are ordered in ascending effective date 
        ### Each entry must have a later effective date than the prior entry 
        ### If any entry year is changed quartely, 
        ### the rate as of January 1st of the following year MUST be stored 

        # 10/1/81-12/31/94	12%	.03333%	.0003333
        self.db.add_rate(
            series_id,
            RateRow(
            effective_date = date(1981, 10, 1),
            annual_rate_percent = 12.0,
            daily_rate_decimal = 0.0003333
            )
        )


        # 1995	8%	.02192%	.0002192
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(1995, 1, 1),
                annual_rate_percent = 8.0,
                daily_rate_decimal = 0.0002192
            )
        )

        # 1996	10%	.02740%	.0002740
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(1996, 1, 1),
                annual_rate_percent = 10.0,
                daily_rate_decimal = 0.0002740
            )
        )

        # 2001	11%	.03014%	.0003014
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2001, 1, 1),
                annual_rate_percent = 11.0,
                daily_rate_decimal = 0.0003014
            )
        )

        # 2002	9%	.02466%	.0002466
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2002, 1, 1),
                annual_rate_percent = 9.0,
                daily_rate_decimal = 0.0002466
            )
        )

        # 2003	6%	.01644%	.0001644
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2003, 1, 1),
                annual_rate_percent = 6.0,
                daily_rate_decimal = 0.0001644
            )
        )

        # 2004	7%	.01918%	.0001918
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2004, 1, 1),
                annual_rate_percent = 7.0,
                daily_rate_decimal = 0.0001918
            )
        )

        # 2006	9%	.02466%	.0002466
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2006, 1, 1),
                annual_rate_percent = 9.0,
                daily_rate_decimal = 0.0002466
            )
        )

        # 2007	11%	.03014%	.0003014
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2007, 1, 1),
                annual_rate_percent = 11.0,
                daily_rate_decimal = 0.0003014
            )
        )

        # 2009	8%	.02192%	.0002192 
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2009, 1, 1),
                annual_rate_percent = 8.0,
                daily_rate_decimal = 0.0002192
            )
        )

        # 2010	6%	.01644%	.0001644
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2010, 1, 1),
                annual_rate_percent = 6.0,
                daily_rate_decimal = 0.0001644
            )
        )

        # 1/1/2011-9/30/11	6%	.01644%	.0001644
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2011, 1, 1),
                annual_rate_percent = 6.0,
                daily_rate_decimal = 0.0001644
            )
        )

        # 10/1/11 - 12/31/2011	4.75%	.0130137%	.000130137
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2011, 10, 1),
                annual_rate_percent = 4.75,
                daily_rate_decimal = 0.000130137
            )
        )

        # 2012	4.75%	.0129781%	.000129781 
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2012, 1, 1),
                annual_rate_percent = 4.75,
                daily_rate_decimal = 0.000129781
            )
        )

        # January 1, 2013	4.75%	.0130137%	.000130137
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2013, 1, 1),
                annual_rate_percent = 4.75,
                daily_rate_decimal = 0.000130137
            )
        )

        # January 1, 2016	4.75%	.0129781%	.000129781
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2016, 1, 1),
                annual_rate_percent = 4.75,
                daily_rate_decimal = 0.000129781
            )
        )

        # April 1, 2016	4.78%	.01306011%	.0001306011
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2016, 4, 1),
                annual_rate_percent = 4.78,
                daily_rate_decimal = 0.0001306011
            )
        )

        # July 1, 2016	4.84%	.01322404%	.0001322404
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2016, 7, 1),
                annual_rate_percent = 4.84,
                daily_rate_decimal = 0.0001322404
            )
        )

        # October 1, 2016	4.91%	.01341530%	.0001341530
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2016, 10, 1),
                annual_rate_percent = 4.91,
                daily_rate_decimal = 0.0001341530
            )
        )

        # January 1, 2017	4.97%	.01361644%	.0001361644
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2017, 1, 1),
                annual_rate_percent = 4.97,
                daily_rate_decimal = 0.0001361644
            )
        )

        # April 1, 2017     5.05%    .01383562%	 .0001383562
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2017, 4, 1),
                annual_rate_percent = 5.05,
                daily_rate_decimal = 0.0001383562
            )
        )

        # July 1, 2017	5.17%	.01416438%	.0001416438
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2017, 7, 1),
                annual_rate_percent = 5.17,
                daily_rate_decimal = 0.0001416438
            )
        )

        # October 1, 2017	5.35%	.0146575%	.000146575
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2017, 10, 1),
                annual_rate_percent = 5.35,
                daily_rate_decimal = 0.000146575
            )
        )

        # January 1, 2018	5.53%	.0151507%	.000151507
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2018, 1, 1),
                annual_rate_percent = 5.53,
                daily_rate_decimal = 0.000151507
            )
        )

        # April 1, 2018	5.72%	.0156712%	.000156712
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2018, 4, 1),
                annual_rate_percent = 5.72,
                daily_rate_decimal = 0.000156712
            )
        )

        # July 1, 2018	5.97%	.0163562%	.000163562
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2018, 7, 1),
                annual_rate_percent = 5.97,
                daily_rate_decimal = 0.000163562
            )
        )

        # October 1, 2018	6.09%	.0166849%	.000166849
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2018, 10, 1),
                annual_rate_percent = 6.09,
                daily_rate_decimal = 0.000166849
            )
        )

        # January 1, 2019	6.33%	.0173425%	.000173425
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2019, 1, 1),
                annual_rate_percent = 6.33,
                daily_rate_decimal = 0.000173425
            )
        )

        # April 1, 2019 	6.57%	.0180000%	.000180000
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2019, 4, 1),
                annual_rate_percent = 6.57,
                daily_rate_decimal = 0.000180000
            )
        )

        # July 1, 2019	6.77%	.0185479%	.000185479
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2019, 7, 1),
                annual_rate_percent = 6.77,
                daily_rate_decimal = 0.000185479
            )
        )

        # October 1, 2019	6.89%	.0188767%	.000188767
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2019, 10, 1),
                annual_rate_percent = 6.89,
                daily_rate_decimal = 0.000188767
            )
        )

        # January 1, 2020	6.83%	.0186612%	.000186612
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2020, 1, 1),
                annual_rate_percent = 6.83,
                daily_rate_decimal = 0.000186612
            )
        )

        # April 1, 2020	6.66%	.0181967%	.000181967
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2020, 4, 1),
                annual_rate_percent = 6.66,
                daily_rate_decimal = 0.000181967
            )
        )

        # July 1, 2020	6.03%	.0164754%	.000164754
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2020, 7, 1),
                annual_rate_percent = 6.03,
                daily_rate_decimal = 0.000164754
            )
        )

        # October 1, 2020	5.37%	.0146721%	.000146721
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2020, 10, 1),
                annual_rate_percent = 5.37,
                daily_rate_decimal = 0.000146721
            )
        )

        # January 1, 2021	4.81%	.0131781%	.000131781
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2021, 1, 1),
                annual_rate_percent = 4.81,
                daily_rate_decimal = 0.000131781
            )
        )

        # April 1, 2021	4.31%	.0118082%	.000118082
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2021, 4, 1),
                annual_rate_percent = 4.31,
                daily_rate_decimal = 0.000118082
            )
        )

        # July 1, 2021	4.25%	.0116438%	.000116438
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2021, 7, 1),
                annual_rate_percent = 4.25,
                daily_rate_decimal = 0.000116438
            )
        )

        # January 1, 2022	4.25%	.0116438%	.000116438
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2022, 1, 1),
                annual_rate_percent = 4.25,
                daily_rate_decimal = 0.000116438
            )
        )

        # July 1, 2022	4.34%	.0118904%	.000118904
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2022, 7, 1),
                annual_rate_percent = 4.34,
                daily_rate_decimal = 0.000118904
            )
        )

        # October 1, 2022	4.75%	.0130137%	.000130137
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2022, 10, 1),
                annual_rate_percent = 4.75,
                daily_rate_decimal = 0.000130137
            )
        )

        # January 1, 2023	5.52%	.0151233%	.000151233
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2023, 1, 1),
                annual_rate_percent = 5.52,
                daily_rate_decimal = 0.000151233
            )
        )

        # April 1, 2023	6.58%	.0180274%	.000180274
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2023, 4, 1),
                annual_rate_percent = 6.58,
                daily_rate_decimal = 0.000180274
            )
        )

        # July 1, 2023	7.69%	.0210685%	.000210685
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2023, 7, 1),
                annual_rate_percent = 7.69,
                daily_rate_decimal = 0.000210685
            )
        )

        # October 1, 2023	8.54%	.0233973%	.000233973
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2023, 10, 1),
                annual_rate_percent = 8.54,
                daily_rate_decimal = 0.000233973
            )
        )

        # January 1, 2024	9.09%	.0248361%	.000248361
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2024, 1, 1),
                annual_rate_percent = 9.09,
                daily_rate_decimal = 0.000248361
            )
        )

        # April 1, 2024	9.34%	.0255191%	.000255191
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2024, 4, 1),
                annual_rate_percent = 9.34,
                daily_rate_decimal = 0.000255191
            )
        )

        # July 1, 2024	9.46%	.0258470%	.000258470
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2024, 7, 1),
                annual_rate_percent = 9.46,
                daily_rate_decimal = 0.000258470
            )
        )

        # October 1, 2024	9.50%	.0259563%	.000259563 
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2024, 10, 1),
                annual_rate_percent = 9.50,
                daily_rate_decimal = 0.000259563
            )
        )

        # January 1, 2025	9.38%	.0256986%	.000256986
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2025, 1, 1),
                annual_rate_percent = 9.38,
                daily_rate_decimal = 0.000256986
            )
        )

        # April 1, 2025	9.15%	.0250685%	.000250685
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2025, 4, 1),
                annual_rate_percent = 9.15,
                daily_rate_decimal = 0.000250685
            )
        )

        # July 1, 2025	8.90%	.0243836%	.000243836
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2025, 7, 1),
                annual_rate_percent = 8.90,
                daily_rate_decimal = 0.000243836
            )
        )

        # October 1, 2025	8.65%	.0236986%	.000236986
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2025, 10, 1),
                annual_rate_percent = 8.65,
                daily_rate_decimal = 0.000236986
            )
        )

        # January 1, 2026	8.44%	.0231233%	.000231233
        self.db.add_rate(
            series_id,
            RateRow(
                effective_date = date(2026, 1, 1),
                annual_rate_percent = 8.44,
                daily_rate_decimal = 0.000231233
            )
        )

    # Main menu
    def run(self):
        self.print_banner()
        while True:
            choice = self.show_menu_and_get_choice()
            if choice == "q":
                break
            self.dispatch(choice)
            
    def show_menu_and_get_choice(self):
        print("\n===== Welcome to CaseFlow =====")
        print()
        print("\n=== Main Menu ===")
        print("1) Interest calculator")
        print("2) Rate look-up")
        print("3) Validate template")
        print("q) Quit")
        return input("Select: ").strip().lower()
    
    def dispatch(self, choice):
        if choice == "1":
            self.compute_interest()
        elif choice == "2":
            self.rate_lookup()
        elif choice == "3":
            self.validate_template()
        elif choice == "q":
            print("Exiting the application.")
    
    ## Prompts user for principal amount, start_date, end_date
    ## Left room for future implementation of 'judgment_date', need to ask about this 
    def compute_interest(self) -> None:
        # Prompt for principle amount
        principal = float(input("Please enter the principal amount:"))

        # Prompt for start date
        start_date = datetime.strptime(
            input("Enter start date (MM/DD/YYYY): ").strip(),
              "%m/%d/%Y"
              ).date()

        ## For now, set start_date == judgment_date
        ## Might be unique in future, in case there's a discrepancy between the two
        judgment_date = start_date

        # Prompt for end date
        end_date = datetime.strptime(
            input("Please enter an end date (MM/DD/YYYY): ").strip(),
                "%m/%d/%Y"
        ).date()

        # Call to calculate_interest
        interest = self.calculate_interest(principal, start_date, end_date, judgment_date)

        print(f"Interest owed: ${interest}")

    ## Calculates interest from data passed in from compute_interest (principal amount, start date, end date and judgment date)
    # NOTE: judgment_date currently equals start_date in this version.
    def calculate_interest(self, principal: float, start_date: date, end_date: date, judgment_date: date) -> float:
        interest = 0.0
        series_id = "FL_POST_JUDGMENT"
        
        ## If judgement date is prior to Oct 1st, 2011, then rate at that date is static throughout duration.
        if start_date < date(2011, 10, 1): 
            rate_row = self.db.get_rate_as_of(series_id, judgment_date)
            if rate_row is None:
                return 0.0

            ## Start/End day inclusive for now
            days_inclusive = (end_date - start_date).days + 1
            interest = principal * rate_row.daily_rate_decimal * days_inclusive
            return round(interest, 2)
        
        ## Else, calculate interest daily and accumulate to overall interest amount.
        current_date = start_date
        while current_date <= end_date:
            rate_row = self.db.get_rate_as_of(series_id, current_date)
            if rate_row is None:
                return 0.0
            
            interest += principal * rate_row.daily_rate_decimal
            ## Start/End day inclusive for now
            current_date += timedelta(days = 1)

        return round(interest, 2)

    # Pulls rates from specific date, outputs as-of date, date rate went into effect, annual rate as percent, and daily rate as decimal.
    def rate_lookup(self):
        series_id = "FL_POST_JUDGMENT"


        while True:
            s = input("\nEnter date (MM/DD/YYYY) or 'b' to go back: ").strip()
            if s.lower() == "b":
                return

            try:
                as_of = datetime.strptime(s, "%m/%d/%Y").date() 
            except ValueError:
                print("Invalid date format. Please use MM/DD/YYYY. Example: 10/01/2011")
                continue

            rate = self.db.get_rate_as_of(series_id, as_of)

            if rate is None:
                print(f"No rate is found on or before {as_of_str}.")
                continue

            # Format for user display only
            # This happens here for readability
            # Future centralization of date formatting in a presentation-layer 'helper' when/if needed when app grows.
            as_of_str = as_of.strftime("%m/%d/%Y")
            effective_str = rate.effective_date.strftime("%m/%d/%Y")

            # Terminal formatting
            label_w = 20
            print(
            f"\n=== Rate Result ===\n"
            # Output work-around mentioned above, here
            f"{'As-of date:':<{label_w}} {as_of_str}\n"
            # And here
            f"{'Rate effective date:':<{label_w}} {effective_str}\n"
            f"{'Annual rate (%):':<{label_w}} {rate.annual_rate_percent}%\n"
            f"{'Daily rate (decimal):':<{label_w}} {rate.daily_rate_decimal}\n"
            )

    # NOTE: Internal sanity check for rate lookup boundaries. Not used in production flow.
    # Pulls rates from specific date, outputs effective date, annual rate as percent, annual rate as decimal, and daily rate as decimal.
    def _test_rate_lookup(self):
        series_id = "FL_POST_JUDGMENT"

        test_dates = [
            date(1981, 9, 30),   # before first rate
            date(1981, 10, 1),   # first effective date
            date(2011, 9, 30),   # day before 10/1/2011 change
            date(2011, 10, 1),   # exact change date
            date(2026, 1, 4),    # after last known rate
    ]

        print("\n=== Rate Lookup Sanity Test ===")
        for d in test_dates:
            rate = self.db.get_rate_as_of(series_id, d)
            if rate is None:
                print(f"{d} -> None")
            else:
                print(
                        f"{d} -> {rate.annual_rate_percent}% "
                        f"(daily {rate.daily_rate_decimal})"
                )


    def validate_template(self):
        print("Validating template... This feature will be added soon.")
        
    def print_banner(self):
        print("""

                 ..............                
           .. -## ###--### #####- ...          
       ...###### ##### ##+ ########-#-.-       
    ...########+.##### ## +#####--######.-.    
   ..##########+-##### #-.###+ +##########.-.  
 ..############# ####.## #- +###############.- 
..############### ### . -####################-.
. ############+ .+#..+ .+######.    .+####### +
- #######- +########  # ####.#########- +#### +
-.##### ########### .##.+###############..###-.
 + ### ########### +#### ###############+ ##.+ 
  +.++.########## +#####+ ##############.-.--  
    +. +######+  #########. ########### .-+    
      -+      -##############-        .+-      
         .++. -#################. -++.         
               -+++++----++++++.               

""")
        print(r"""     _               _  __             _        ___                          ___    _     
  _ │ │___ _ _  _ _ (_)╱ _│___ _ _    ╱_╲      ╱ __│__ _ _ _ _ _  ___ _ _   │ _ ╲  ╱_╲    
 │ ││ ╱ ─_) ' ╲│ ' ╲│ │  _╱ ─_) '_│  ╱ _ ╲ _  │ (_ ╱ _` │ '_│ ' ╲╱ ─_) '_│  │  _╱ ╱ _ ╲ _ 
  ╲__╱╲___│_││_│_││_│_│_│ ╲___│_│   ╱_╱ ╲_(_)  ╲___╲__,_│_│ │_││_╲___│_│( ) │_│(_)_╱ ╲_(_)
                                                                        │╱                """)
        
def main():

    app = App()

    # Sanity check 
    # app._test_rate_lookup()

    app.run()
            
            

                
            
if __name__ == "__main__":
    main()
	