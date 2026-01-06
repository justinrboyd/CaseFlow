# CaseFlow

CaseFlow is a small but growing command-line tool designed to help automate common tasks in a legal office.

The current focus of the project is accurate Florida post-judgment interest calculations and interest rate lookups based on effective dates. The long-term goal is to expand CaseFlow into a flexible set of utilities that reduce manual work and repetitive calculations.

This project is actively evolving and is being built incrementally, with each feature added in a working and testable state.

## Current Features

- Florida post-judgment interest calculator
- Accurate daily interest calculation using effective rate changes
- Rate lookup by date, showing:
  - as-of date
  - rate effective date
  - annual rate
  - daily rate
- Interactive terminal menu interface

## How It Works

CaseFlow maintains a structured, date-ordered database of Florida post-judgment interest rates.

When calculating interest, the program:
- Applies a single static rate for judgments prior to October 1, 2011
- Applies daily rate changes for dates after that point
- Accumulates interest day-by-day for accuracy
- Rounds results to the nearest cent at the end of the calculation

All date input and output uses standard legal formatting (MM/DD/YYYY).

## Running the Program

This project currently runs as a terminal application.

From the project directory:

python main.py

You will be presented with a menu to:
- calculate interest
- look up interest rates
- access placeholder features planned for future versions

## Project Status

This is an early but stable foundation.

The following are intentionally left for future development:
- Graphical user interface (GUI)
- Document merge and template tools
- Exportable reports
- Windows executable distribution
- Additional automation utilities

Code cleanup, refactoring, and modularization will happen as the feature set grows.

## Disclaimer

This tool is intended to assist with calculations and workflow efficiency.
It does not provide legal advice and should always be used alongside official sources and professional judgment.
