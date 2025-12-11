"""
Mutually Assured Success (MAS) Economic Simulation System
==========================================================

This simulation models economic policy decisions as "offensive/defensive maneuvers"
that create positive-sum outcomes rather than zero-sum conflicts.

The metaphor: Just as Mutually Assured Destruction (MAD) stabilized the Cold War
through the threat of catastrophic mutual harm, Mutually Assured Success (MAS)
stabilizes economic systems through the guarantee of shared minimum prosperity.

Key Parameters:
- Import Share: Percentage of GDP from imports (defensive posture indicator)
- Tariff Rates: Trade policy tool (can be offensive or defensive)
- Digital Services Tax (DST) Rates: Tax on tech platforms (revenue + competition tool)
- Universal Energy Dividend (UED): Direct transfer to citizens (prosperity floor)

Outputs:
- Inflation Impact: How policy choices affect price levels
- Revenue Estimates: Government revenue from tariffs and DST
- Economic Growth: GDP impact of policy combinations
- Poverty Reduction: Impact on poverty rates
- MAS Score: Overall positive-sum outcome measure
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass
from itertools import product


@dataclass
class EconomicScenario:
    """Represents a single economic policy scenario"""
    scenario_id: str
    import_share: float  # Percentage of GDP from imports (0-100)
    tariff_rate: float  # Tariff rate as percentage (0-50)
    dst_rate: float  # Digital Services Tax rate (0-10)
    ued_per_capita: float  # Universal Energy Dividend per person (USD)
    
    def __post_init__(self):
        """Validate inputs"""
        assert 0 <= self.import_share <= 100, "Import share must be 0-100%"
        assert 0 <= self.tariff_rate <= 50, "Tariff rate must be 0-50%"
        assert 0 <= self.dst_rate <= 10, "DST rate must be 0-10%"
        assert self.ued_per_capita >= 0, "UED must be non-negative"


class MASEconomicSimulator:
    """
    Simulates economic outcomes under different policy combinations.
    
    The "offensive/defensive maneuvers" metaphor:
    - Offensive: Policies that create new value (UED, investment, innovation)
    - Defensive: Policies that protect existing value (tariffs, regulations)
    - MAS: Policies that ensure both sides benefit (positive-sum outcomes)
    """
    
    def __init__(
        self,
        base_gdp: float = 25_000_000_000_000,  # $25 trillion (US GDP)
        population: int = 330_000_000,  # US population
        base_inflation: float = 2.5,  # Base inflation rate (%)
        tech_platform_revenue: float = 1_500_000_000_000,  # Tech platform revenue
        import_value_base: float = 3_000_000_000_000,  # Base import value
    ):
        self.base_gdp = base_gdp
        self.population = population
        self.base_inflation = base_inflation
        self.tech_platform_revenue = tech_platform_revenue
        self.import_value_base = import_value_base
        
    def calculate_inflation_impact(
        self,
        scenario: EconomicScenario
    ) -> float:
        """
        Calculate inflation impact of policy choices.
        
        Inflation drivers:
        - Tariffs increase import costs → higher prices
        - UED increases demand → potential price pressure
        - DST may be passed to consumers → price increase
        - But UED also increases supply capacity → price moderation
        """
        inflation_impact = self.base_inflation
        
        # Tariff impact: tariffs increase import costs
        # Assumes 40% of tariff cost is passed to consumers
        tariff_inflation = scenario.tariff_rate * 0.4 * (scenario.import_share / 100) * 0.3
        inflation_impact += tariff_inflation
        
        # DST impact: tech platforms may pass some costs to consumers
        # Assumes 30% pass-through, affects 15% of consumer spending
        dst_inflation = scenario.dst_rate * 0.3 * 0.15 * 0.2
        inflation_impact += dst_inflation
        
        # UED impact: increases demand but also supply capacity
        # Net effect: slight demand increase, but supply response moderates
        ued_demand_effect = (scenario.ued_per_capita / 1000) * 0.1  # Demand increase
        ued_supply_effect = (scenario.ued_per_capita / 1000) * 0.08  # Supply increase
        ued_net_inflation = (ued_demand_effect - ued_supply_effect) * 0.5
        inflation_impact += ued_net_inflation
        
        return round(inflation_impact, 2)
    
    def calculate_revenue(
        self,
        scenario: EconomicScenario
    ) -> Dict[str, float]:
        """
        Calculate government revenue from tariffs and DST.
        
        Revenue sources:
        - Tariff revenue: tariff_rate * import_value
        - DST revenue: dst_rate * tech_platform_revenue
        - UED cost: negative revenue (transfer to citizens)
        """
        # Import value scales with import share
        import_value = self.import_value_base * (scenario.import_share / 30)  # Normalize to 30% baseline
        
        # Tariff revenue
        tariff_revenue = (scenario.tariff_rate / 100) * import_value
        
        # DST revenue
        dst_revenue = (scenario.dst_rate / 100) * self.tech_platform_revenue
        
        # UED cost (negative revenue)
        ued_cost = scenario.ued_per_capita * self.population
        
        # Net revenue
        total_revenue = tariff_revenue + dst_revenue
        net_revenue = total_revenue - ued_cost
        
        return {
            'tariff_revenue': round(tariff_revenue / 1e9, 2),  # Billions
            'dst_revenue': round(dst_revenue / 1e9, 2),  # Billions
            'ued_cost': round(ued_cost / 1e9, 2),  # Billions
            'total_revenue': round(total_revenue / 1e9, 2),  # Billions
            'net_revenue': round(net_revenue / 1e9, 2),  # Billions
        }
    
    def calculate_gdp_impact(
        self,
        scenario: EconomicScenario
    ) -> float:
        """
        Calculate GDP growth impact.
        
        GDP drivers:
        - Tariffs: negative (reduces trade efficiency)
        - DST: neutral to slightly positive (redistributes, doesn't destroy)
        - UED: positive (increases consumption and investment)
        """
        gdp_growth = 0.0
        
        # Tariff impact: reduces trade efficiency
        # -1% GDP growth per 10% tariff (diminishing returns)
        tariff_gdp_impact = -(scenario.tariff_rate / 10) * 0.5
        gdp_growth += tariff_gdp_impact
        
        # DST impact: neutral (redistribution, not destruction)
        # Slight positive from increased government spending
        dst_gdp_impact = (scenario.dst_rate / 10) * 0.1
        gdp_growth += dst_gdp_impact
        
        # UED impact: strong positive (multiplier effect)
        # $1 UED → $1.5-2.0 GDP (consumption multiplier)
        ued_multiplier = 1.7
        ued_gdp_impact = ((scenario.ued_per_capita * self.population) / self.base_gdp) * ued_multiplier * 100
        gdp_growth += ued_gdp_impact
        
        return round(gdp_growth, 2)
    
    def calculate_poverty_reduction(
        self,
        scenario: EconomicScenario
    ) -> float:
        """
        Calculate poverty rate reduction.
        
        Poverty reduction drivers:
        - UED: direct impact (guaranteed income floor)
        - GDP growth: indirect impact (job creation)
        - Tariffs: mixed (protects jobs but increases costs)
        """
        base_poverty_rate = 11.5  # Current US poverty rate
        
        # UED direct impact: lifts people above poverty line
        # Poverty line: ~$13,000 for individual
        ued_poverty_reduction = min(
            (scenario.ued_per_capita / 13000) * 2.0,  # Can reduce poverty by up to 2x UED ratio
            8.0  # Maximum 8 percentage point reduction
        )
        
        # GDP growth indirect impact
        gdp_impact = self.calculate_gdp_impact(scenario)
        gdp_poverty_reduction = max(gdp_impact * 0.3, 0)  # 0.3% poverty reduction per 1% GDP growth
        
        # Tariff impact: protects some jobs but increases costs
        # Net: slight positive (job protection > cost increase for low-income)
        tariff_poverty_impact = (scenario.tariff_rate / 10) * 0.1
        
        total_reduction = ued_poverty_reduction + gdp_poverty_reduction + tariff_poverty_impact
        new_poverty_rate = max(base_poverty_rate - total_reduction, 0)
        
        return round(new_poverty_rate, 2)
    
    def calculate_mas_score(
        self,
        scenario: EconomicScenario
    ) -> float:
        """
        Calculate Mutually Assured Success (MAS) score.
        
        MAS Score = weighted combination of:
        - Low inflation (stability)
        - Positive revenue (sustainability)
        - GDP growth (prosperity)
        - Poverty reduction (inclusion)
        - Positive-sum outcomes (all benefit)
        
        Score range: 0-100
        - 80-100: Strong MAS (all benefit significantly)
        - 60-79: Moderate MAS (most benefit)
        - 40-59: Weak MAS (some benefit, some lose)
        - 0-39: Zero-sum or negative-sum (conflict)
        """
        inflation = self.calculate_inflation_impact(scenario)
        revenue = self.calculate_revenue(scenario)
        gdp_growth = self.calculate_gdp_impact(scenario)
        poverty_rate = self.calculate_poverty_reduction(scenario)
        
        # Normalize components (0-100 scale)
        # Inflation: lower is better (target: 2-3%)
        inflation_score = max(0, 100 - (inflation - 2.0) * 20) if inflation <= 5 else max(0, 100 - (inflation - 5) * 10)
        
        # Revenue: positive net is good, but not required if UED is high
        # Score based on sustainability (can maintain policy)
        revenue_score = min(100, 50 + (revenue['net_revenue'] / 100) * 10) if revenue['net_revenue'] >= -500 else 30
        
        # GDP growth: positive is good
        gdp_score = min(100, 50 + gdp_growth * 5)
        
        # Poverty reduction: lower poverty is better
        poverty_score = min(100, (11.5 - poverty_rate) / 11.5 * 100)
        
        # Positive-sum bonus: if all metrics improve, add bonus
        positive_sum_bonus = 0
        if gdp_growth > 0 and poverty_rate < 11.5 and inflation < 4:
            positive_sum_bonus = 10
        
        # Weighted average
        mas_score = (
            inflation_score * 0.25 +
            revenue_score * 0.20 +
            gdp_score * 0.25 +
            poverty_score * 0.30 +
            positive_sum_bonus
        )
        
        return round(mas_score, 2)
    
    def simulate_scenario(
        self,
        scenario: EconomicScenario
    ) -> Dict:
        """Run complete simulation for a single scenario"""
        return {
            'scenario_id': scenario.scenario_id,
            'import_share': scenario.import_share,
            'tariff_rate': scenario.tariff_rate,
            'dst_rate': scenario.dst_rate,
            'ued_per_capita': scenario.ued_per_capita,
            'inflation_impact': self.calculate_inflation_impact(scenario),
            'revenue': self.calculate_revenue(scenario),
            'gdp_growth': self.calculate_gdp_impact(scenario),
            'poverty_rate': self.calculate_poverty_reduction(scenario),
            'mas_score': self.calculate_mas_score(scenario),
        }
    
    def generate_decision_table(
        self,
        import_shares: List[float] = [15, 20, 25, 30],
        tariff_rates: List[float] = [0, 5, 10, 15],
        dst_rates: List[float] = [0, 3, 5, 7],
        ued_levels: List[float] = [0, 1000, 2000, 3000],
        max_scenarios: int = 50  # Limit for readability
    ) -> pd.DataFrame:
        """
        Generate decision table with all parameter combinations.
        
        This represents the "offensive/defensive maneuver" space:
        - Different combinations of policy tools
        - Each combination produces different outcomes
        - MAS score identifies positive-sum solutions
        """
        scenarios = []
        scenario_count = 0
        
        # Generate all combinations
        for import_share, tariff_rate, dst_rate, ued in product(
            import_shares, tariff_rates, dst_rates, ued_levels
        ):
            if scenario_count >= max_scenarios:
                break
                
            scenario = EconomicScenario(
                scenario_id=f"S{scenario_count + 1:03d}",
                import_share=import_share,
                tariff_rate=tariff_rate,
                dst_rate=dst_rate,
                ued_per_capita=ued,
            )
            
            result = self.simulate_scenario(scenario)
            scenarios.append(result)
            scenario_count += 1
        
        # Convert to DataFrame
        df = pd.DataFrame(scenarios)
        
        # Flatten revenue dictionary
        revenue_cols = ['tariff_revenue', 'dst_revenue', 'ued_cost', 'total_revenue', 'net_revenue']
        for col in revenue_cols:
            df[col] = df['revenue'].apply(lambda x: x[col])
        df = df.drop('revenue', axis=1)
        
        # Sort by MAS score (best first)
        df = df.sort_values('mas_score', ascending=False).reset_index(drop=True)
        
        return df
    
    def print_decision_table(
        self,
        df: pd.DataFrame,
        top_n: int = 20
    ):
        """Print formatted decision table"""
        print("\n" + "="*120)
        print("MUTUALLY ASSURED SUCCESS (MAS) ECONOMIC SIMULATION - DECISION TABLE")
        print("="*120)
        print("\nMetaphor: Economic policy as 'offensive/defensive maneuvers'")
        print("Goal: Identify positive-sum outcomes where all parties benefit")
        print("\n" + "-"*120)
        
        # Display top scenarios
        top_df = df.head(top_n).copy()
        
        # Format for display
        display_cols = [
            'scenario_id',
            'import_share', 'tariff_rate', 'dst_rate', 'ued_per_capita',
            'inflation_impact', 'gdp_growth', 'poverty_rate', 'mas_score',
            'net_revenue'
        ]
        
        print(f"\nTop {top_n} Scenarios (sorted by MAS Score):\n")
        print(top_df[display_cols].to_string(index=False))
        
        print("\n" + "-"*120)
        print("KEY METRICS:")
        print(f"  - Inflation Impact: Target 2-3% (lower is better)")
        print(f"  - GDP Growth: Positive is better")
        print(f"  - Poverty Rate: Lower is better (current baseline: 11.5%)")
        print(f"  - MAS Score: 80-100 = Strong MAS (all benefit), 60-79 = Moderate, <60 = Weak")
        print(f"  - Net Revenue: Can be negative if UED > revenue (sustainability consideration)")
        print("\n" + "="*120)
        
        # Summary statistics
        print("\nSUMMARY STATISTICS:")
        print(f"  Best MAS Score: {df['mas_score'].max():.2f}")
        print(f"  Average MAS Score: {df['mas_score'].mean():.2f}")
        print(f"  Scenarios with MAS > 80: {(df['mas_score'] > 80).sum()}")
        print(f"  Scenarios with MAS > 60: {(df['mas_score'] > 60).sum()}")
        print(f"  Scenarios with positive GDP growth: {(df['gdp_growth'] > 0).sum()}")
        print(f"  Scenarios with poverty reduction: {(df['poverty_rate'] < 11.5).sum()}")
        
        return top_df


def main():
    """Run MAS economic simulations"""
    
    # Initialize simulator
    simulator = MASEconomicSimulator()
    
    # Generate decision table
    print("Generating MAS Economic Simulation Decision Table...")
    print("This may take a moment...\n")
    
    df = simulator.generate_decision_table(
        import_shares=[15, 20, 25, 30],
        tariff_rates=[0, 5, 10, 15],
        dst_rates=[0, 3, 5, 7],
        ued_levels=[0, 1000, 2000, 3000],
        max_scenarios=50
    )
    
    # Print results
    top_df = simulator.print_decision_table(df, top_n=20)
    
    # Save to CSV
    output_file = "mas_economic_decision_table.csv"
    df.to_csv(output_file, index=False)
    print(f"\nFull decision table saved to: {output_file}")
    
    # Analyze best scenarios
    print("\n" + "="*120)
    print("ANALYSIS: Best MAS Scenarios")
    print("="*120)
    
    best_scenarios = df[df['mas_score'] > 80].head(5)
    
    if len(best_scenarios) > 0:
        print("\nCharacteristics of Top MAS Scenarios (>80 score):")
        print(f"  Average UED: ${best_scenarios['ued_per_capita'].mean():.0f} per capita")
        print(f"  Average Tariff Rate: {best_scenarios['tariff_rate'].mean():.1f}%")
        print(f"  Average DST Rate: {best_scenarios['dst_rate'].mean():.1f}%")
        print(f"  Average Inflation: {best_scenarios['inflation_impact'].mean():.2f}%")
        print(f"  Average GDP Growth: {best_scenarios['gdp_growth'].mean():.2f}%")
        print(f"  Average Poverty Rate: {best_scenarios['poverty_rate'].mean():.2f}%")
    else:
        print("\nNo scenarios achieved MAS score > 80")
        print("Consider adjusting parameters or accepting trade-offs")
    
    return df, top_df


if __name__ == "__main__":
    df, top_df = main()

