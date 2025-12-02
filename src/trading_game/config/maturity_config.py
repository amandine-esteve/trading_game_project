"""
Maturity configuration for options trading.

Defines standard market maturities and provides helper functions to calculate
expiration dates and business days according to market conventions:
- Weekly maturities: Business days only
- Monthly/Annual maturities: 3rd Friday of target month
- Quarterly maturities (LEAPS): 3rd Friday of Mar/Jun/Sep/Dec, only if > 1Y from today
"""

from datetime import datetime, timedelta
from typing import List, Tuple
import calendar


def get_third_friday(year: int, month: int) -> datetime:
    """
    Get the 3rd Friday of a given month/year.
    
    Args:
        year: Target year
        month: Target month (1-12)
    
    Returns:
        datetime object for 3rd Friday at midnight
    """
    # Get first day of the month
    first_day = datetime(year, month, 1)
    
    # Find the first Friday
    # weekday(): Monday=0, Sunday=6, so Friday=4
    days_until_friday = (4 - first_day.weekday()) % 7
    first_friday = first_day + timedelta(days=days_until_friday)
    
    # Add 2 weeks to get the 3rd Friday
    third_friday = first_friday + timedelta(weeks=2)
    
    return third_friday


def count_business_days(start_date: datetime, end_date: datetime) -> int:
    """
    Count business days between two dates (excluding weekends).
    
    Args:
        start_date: Starting date
        end_date: Ending date
    
    Returns:
        Number of business days (excluding Saturdays and Sundays)
    """
    business_days = 0
    current_date = start_date
    
    while current_date < end_date:
        # weekday(): Monday=0, Sunday=6
        # Saturday=5, Sunday=6
        if current_date.weekday() < 5:  # Monday to Friday
            business_days += 1
        current_date += timedelta(days=1)
    
    return business_days


def add_business_days(start_date: datetime, business_days: int) -> datetime:
    """
    Add a number of business days to a date.
    
    Args:
        start_date: Starting date
        business_days: Number of business days to add
    
    Returns:
        End date after adding business days
    """
    current_date = start_date
    days_added = 0
    
    while days_added < business_days:
        current_date += timedelta(days=1)
        # Only count weekdays
        if current_date.weekday() < 5:
            days_added += 1
    
    return current_date


def get_maturity_date_and_days(maturity_label: str, reference_date: datetime = None) -> Tuple[datetime, int]:
    """
    Calculate expiration date and business days for a maturity label.
    
    Args:
        maturity_label: "1W", "2W", "1M", "2M", "3M", "6M", "9M", "1Y", or "Mar-2026", etc.
        reference_date: Starting date (defaults to today)
    
    Returns:
        (expiration_date, business_days_count)
    """
    if reference_date is None:
        reference_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Weekly: Add business days
    if maturity_label in ["1W", "2W"]:
        days_to_add = 5 if maturity_label == "1W" else 10  # 1 or 2 business weeks
        expiry_date = add_business_days(reference_date, days_to_add)
        business_days = days_to_add
        
    # Monthly/Annual: Find 3rd Friday of target month
    elif maturity_label in ["1M", "2M", "3M", "6M", "9M", "1Y"]:
        months_map = {"1M": 1, "2M": 2, "3M": 3, "6M": 6, "9M": 9, "1Y": 12}
        months_ahead = months_map[maturity_label]
        
        # Calculate target month/year
        target_month = reference_date.month + months_ahead
        target_year = reference_date.year
        
        # Handle year overflow
        while target_month > 12:
            target_month -= 12
            target_year += 1
        
        expiry_date = get_third_friday(target_year, target_month)
        business_days = count_business_days(reference_date, expiry_date)
        
    # Quarterly: "Mar-2026" format
    else:
        month_str, year_str = maturity_label.split("-")
        month_map = {"Mar": 3, "Jun": 6, "Sep": 9, "Dec": 12}
        expiry_date = get_third_friday(int(year_str), month_map[month_str])
        business_days = count_business_days(reference_date, expiry_date)
    
    return expiry_date, business_days


def get_maturity_options(
    include_weeklies: bool = True,
    include_monthlies: bool = True, 
    include_quarterlies: bool = True,
    max_years: int = 5,
    reference_date: datetime = None
) -> List[Tuple[str, int]]:
    """
    Returns list of (label, business_days) tuples for maturity selection.
    
    Quarterly options only include dates > 1Y from today and don't duplicate monthly/annual maturities.
    
    Args:
        include_weeklies: Include 1W, 2W options
        include_monthlies: Include 1M-9M, 1Y options
        include_quarterlies: Include quarterly LEAPS (Mar/Jun/Sep/Dec)
        max_years: Maximum years ahead for quarterly options
        reference_date: Reference date (defaults to today)
    
    Returns:
        List of (label, business_days) tuples
    """
    options = []
    monthly_expiry_dates = set()  # Track monthly/annual expiry dates to avoid duplicates
    
    if reference_date is None:
        reference_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    if include_weeklies:
        for label in ["1W", "2W"]:
            _, days = get_maturity_date_and_days(label, reference_date)
            options.append((label, days))
    
    if include_monthlies:
        for label in ["1M", "2M", "3M", "6M", "9M", "1Y"]:
            expiry_date, days = get_maturity_date_and_days(label, reference_date)
            options.append((label, days))
            monthly_expiry_dates.add(expiry_date.date())  # Store date (not datetime) for comparison
    
    if include_quarterlies:
        # Calculate 1 year from reference date
        one_year_ahead = reference_date + timedelta(days=365)
        
        # Generate quarterly expirations for next max_years
        for year_offset in range(max_years + 1):
            for month_name, month_num in [("Mar", 3), ("Jun", 6), ("Sep", 9), ("Dec", 12)]:
                target_year = reference_date.year + year_offset
                expiry_date = get_third_friday(target_year, month_num)
                
                # Only include if > 1 year from reference date AND not already in monthly/annual maturities
                if expiry_date > one_year_ahead and expiry_date.date() not in monthly_expiry_dates:
                    label = f"{month_name}-{target_year}"
                    business_days = count_business_days(reference_date, expiry_date)
                    options.append((label, business_days))
    
    return options



def get_short_maturity_options(reference_date: datetime = None) -> List[Tuple[str, int]]:
    """
    Get maturity options suitable for short leg of calendar spreads.
    Includes weeklies and monthlies up to 1Y.
    
    Returns:
        List of (label, business_days) tuples
    """
    return get_maturity_options(
        include_weeklies=True,
        include_monthlies=True,
        include_quarterlies=False,
        reference_date=reference_date
    )


def get_long_maturity_options(reference_date: datetime = None) -> List[Tuple[str, int]]:
    """
    Get maturity options suitable for long leg of calendar spreads.
    Includes monthlies and quarterlies up to 2 years.
    
    Returns:
        List of (label, business_days) tuples
    """
    return get_maturity_options(
        include_weeklies=False,
        include_monthlies=True,
        include_quarterlies=True,
        max_years=2,
        reference_date=reference_date
    )
