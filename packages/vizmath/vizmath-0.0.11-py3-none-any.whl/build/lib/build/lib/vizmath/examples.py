
# Examples

#region Nick's Radial Treemap
#%%
import radial_treemap as rtm
import pandas as pd
data = [
    ['a1', 'b1', 'c1', 12.3],
    ['a1', 'b2', 'c1', 4.5],
    ['a2', 'b1', 'c2', 32.3],
    ['a1', 'b2', 'c2', 2.1],
    ['a2', 'b1', 'c1', 5.9],
    ['a3', 'b1', 'c1', 3.5],
    ['a4', 'b2', 'c1', 3.1]]
df = pd.DataFrame(data, columns = ['a', 'b', 'c', 'value'])
o_rtm = rtm.rad_treemap(df, ['a','b','c'], 'value', 0.5, 1, 0, 180, 200,
    rotate_deg=-90, mode='alternate', default_sort_override_reversed=True, no_groups=False)
#%%
o_rtm.plot_levels(3, 0.5)
#%%
o_rtm.to_df().head()
#endregion
