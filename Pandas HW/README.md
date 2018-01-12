
PyCity Schools Analysis

Observation1: Charter schools outperform district schools in every category
Observation2: Large schools have the worst performance; medium and small are close to the same, but both outperform larger schools.
Observation3: Charter schools also appear to be more efficient with their budgets.  Despite having lower per-student budgets overall, they are able to get better results.  I would guess this is due to charter schools generally being smaller in size which would lead to less overhead. 


```python
import pandas as pd
import os
import csv
```


```python
data_file = os.path.join("schools_complete.csv")
data_file2 = os.path.join("students_complete.csv")

schools = pd.read_csv(data_file)
students = pd.read_csv(data_file2)
```


```python
total_schools = len(schools)
total_students = students["name"].count()
total_budget = schools["budget"].sum()
avg_math_score = students["math_score"].mean()
avg_reading_score = students["reading_score"].mean()
math_pass = students[(students['math_score']>70)].count()['name']
reading_pass = students[(students['reading_score']>70)].count()['name']
math_pass_perc = (math_pass / total_students) * 100
reading_pass_perc = (reading_pass / total_students) * 100
overall_pass_perc = (reading_pass_perc + math_pass_perc)/2
```


```python
district_summary = pd.DataFrame({"Total Schools": [total_schools],
                               "Total Students": [total_students],
                               "Total Budget": [total_budget],
                               "Average Math Score": [avg_math_score],
                               "Average Reading Score": [avg_reading_score],
                               "% Passing Math": [math_pass_perc],
                               "% Passing Reading": [reading_pass_perc],
                               "% Overall Passing Rate": [overall_pass_perc]})

district_summary["Total Budget"] = district_summary["Total Budget"].map("${0:,.0f}".format)
district_summary["% Overall Passing Rate"] = district_summary["% Overall Passing Rate"].map("{0:,.2f}%".format)
district_summary["% Passing Reading"] = district_summary["% Passing Reading"].map("{0:,.2f}%".format)
district_summary = district_summary.round(2)
district_summary
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>% Overall Passing Rate</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>Total Budget</th>
      <th>Total Schools</th>
      <th>Total Students</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>77.68%</td>
      <td>72.39%</td>
      <td>82.97%</td>
      <td>78.99</td>
      <td>81.88</td>
      <td>$24,649,428</td>
      <td>15</td>
      <td>39170</td>
    </tr>
  </tbody>
</table>
</div>




```python
students = students.rename(columns = {"school" : "school name"})
schools = schools.rename(columns = {"name": "school name"})

combined_df = pd.merge(schools, students, on="school name", how="inner")
combined_df.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>School ID</th>
      <th>school name</th>
      <th>type</th>
      <th>size</th>
      <th>budget</th>
      <th>Student ID</th>
      <th>name</th>
      <th>gender</th>
      <th>grade</th>
      <th>reading_score</th>
      <th>math_score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>Huang High School</td>
      <td>District</td>
      <td>2917</td>
      <td>1910635</td>
      <td>0</td>
      <td>Paul Bradley</td>
      <td>M</td>
      <td>9th</td>
      <td>66</td>
      <td>79</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0</td>
      <td>Huang High School</td>
      <td>District</td>
      <td>2917</td>
      <td>1910635</td>
      <td>1</td>
      <td>Victor Smith</td>
      <td>M</td>
      <td>12th</td>
      <td>94</td>
      <td>61</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0</td>
      <td>Huang High School</td>
      <td>District</td>
      <td>2917</td>
      <td>1910635</td>
      <td>2</td>
      <td>Kevin Rodriguez</td>
      <td>M</td>
      <td>12th</td>
      <td>90</td>
      <td>60</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0</td>
      <td>Huang High School</td>
      <td>District</td>
      <td>2917</td>
      <td>1910635</td>
      <td>3</td>
      <td>Dr. Richard Scott</td>
      <td>M</td>
      <td>12th</td>
      <td>67</td>
      <td>58</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0</td>
      <td>Huang High School</td>
      <td>District</td>
      <td>2917</td>
      <td>1910635</td>
      <td>4</td>
      <td>Bonnie Ray</td>
      <td>F</td>
      <td>9th</td>
      <td>97</td>
      <td>84</td>
    </tr>
  </tbody>
</table>
</div>




```python
school_summary = combined_df.groupby(['school name'], as_index=False)

avg_school_math_score = pd.DataFrame(school_summary['math_score'].mean())
avg_school_reading_score = pd.DataFrame(school_summary['reading_score'].mean())
avg_school_math_score.columns = ['school name', 'avg_school_math']

avg_school_reading_score.columns = ['school name', 'avg_school_reading']

```


```python
school_math_pass = students[students['math_score']>70].groupby(['school name'])
school_math_pass_df = pd.DataFrame(school_math_pass['math_score'].count())

perc_passing_math = combined_df[combined_df['math_score']>=70].groupby(['school name'])
perc_passing_math_df = pd.DataFrame(perc_passing_math['math_score'].count())
perc_passing_math_df.reset_index(inplace=True)

school_reading_pass = students[students['reading_score']>70].groupby(['school name'])
school_reading_pass_df = pd.DataFrame(school_reading_pass['reading_score'].count())

perc_passing_reading = combined_df[combined_df['reading_score']>=70].groupby(['school name'])
perc_passing_reading_df = pd.DataFrame(perc_passing_reading['reading_score'].count())
perc_passing_reading_df.reset_index(inplace=True)


merged_df = pd.merge(avg_school_math_score, avg_school_reading_score, on="school name", how="outer")
merged_df = pd.merge(merged_df, schools, on="school name", how="outer")
merged_df = pd.merge(merged_df, perc_passing_math_df, on="school name", how="outer")
merged_df = pd.merge(merged_df, perc_passing_reading_df, on="school name", how="outer")


merged_df["Per Student Budget"] = (merged_df["budget"] / merged_df["size"])
merged_df["% Passing Math"] = (merged_df["math_score"] / merged_df["size"]) *100
merged_df["% Passing Reading"] = (merged_df["reading_score"] / merged_df["size"]) * 100
merged_df["% Overall Passing Rate"] = ((merged_df["% Passing Math"] + merged_df["% Passing Reading"]) /2)

                     
del merged_df['math_score']
del merged_df['reading_score']
del merged_df['School ID']
merged_df = merged_df.rename(columns = {"avg_school_math":"Average Math Score", "avg_school_reading":"Average Reading Score","type":"School Type","size":"Total Students","budget":"Total School Budget", "school name":"School Name",})
merged_df
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>School Name</th>
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>School Type</th>
      <th>Total Students</th>
      <th>Total School Budget</th>
      <th>Per Student Budget</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>% Overall Passing Rate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Bailey High School</td>
      <td>77.048432</td>
      <td>81.033963</td>
      <td>District</td>
      <td>4976</td>
      <td>3124928</td>
      <td>628.0</td>
      <td>66.680064</td>
      <td>81.933280</td>
      <td>74.306672</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Cabrera High School</td>
      <td>83.061895</td>
      <td>83.975780</td>
      <td>Charter</td>
      <td>1858</td>
      <td>1081356</td>
      <td>582.0</td>
      <td>94.133477</td>
      <td>97.039828</td>
      <td>95.586652</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Figueroa High School</td>
      <td>76.711767</td>
      <td>81.158020</td>
      <td>District</td>
      <td>2949</td>
      <td>1884411</td>
      <td>639.0</td>
      <td>65.988471</td>
      <td>80.739234</td>
      <td>73.363852</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Ford High School</td>
      <td>77.102592</td>
      <td>80.746258</td>
      <td>District</td>
      <td>2739</td>
      <td>1763916</td>
      <td>644.0</td>
      <td>68.309602</td>
      <td>79.299014</td>
      <td>73.804308</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Griffin High School</td>
      <td>83.351499</td>
      <td>83.816757</td>
      <td>Charter</td>
      <td>1468</td>
      <td>917500</td>
      <td>625.0</td>
      <td>93.392371</td>
      <td>97.138965</td>
      <td>95.265668</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Hernandez High School</td>
      <td>77.289752</td>
      <td>80.934412</td>
      <td>District</td>
      <td>4635</td>
      <td>3022020</td>
      <td>652.0</td>
      <td>66.752967</td>
      <td>80.862999</td>
      <td>73.807983</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Holden High School</td>
      <td>83.803279</td>
      <td>83.814988</td>
      <td>Charter</td>
      <td>427</td>
      <td>248087</td>
      <td>581.0</td>
      <td>92.505855</td>
      <td>96.252927</td>
      <td>94.379391</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Huang High School</td>
      <td>76.629414</td>
      <td>81.182722</td>
      <td>District</td>
      <td>2917</td>
      <td>1910635</td>
      <td>655.0</td>
      <td>65.683922</td>
      <td>81.316421</td>
      <td>73.500171</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Johnson High School</td>
      <td>77.072464</td>
      <td>80.966394</td>
      <td>District</td>
      <td>4761</td>
      <td>3094650</td>
      <td>650.0</td>
      <td>66.057551</td>
      <td>81.222432</td>
      <td>73.639992</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Pena High School</td>
      <td>83.839917</td>
      <td>84.044699</td>
      <td>Charter</td>
      <td>962</td>
      <td>585858</td>
      <td>609.0</td>
      <td>94.594595</td>
      <td>95.945946</td>
      <td>95.270270</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Rodriguez High School</td>
      <td>76.842711</td>
      <td>80.744686</td>
      <td>District</td>
      <td>3999</td>
      <td>2547363</td>
      <td>637.0</td>
      <td>66.366592</td>
      <td>80.220055</td>
      <td>73.293323</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Shelton High School</td>
      <td>83.359455</td>
      <td>83.725724</td>
      <td>Charter</td>
      <td>1761</td>
      <td>1056600</td>
      <td>600.0</td>
      <td>93.867121</td>
      <td>95.854628</td>
      <td>94.860875</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Thomas High School</td>
      <td>83.418349</td>
      <td>83.848930</td>
      <td>Charter</td>
      <td>1635</td>
      <td>1043130</td>
      <td>638.0</td>
      <td>93.272171</td>
      <td>97.308869</td>
      <td>95.290520</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Wilson High School</td>
      <td>83.274201</td>
      <td>83.989488</td>
      <td>Charter</td>
      <td>2283</td>
      <td>1319574</td>
      <td>578.0</td>
      <td>93.867718</td>
      <td>96.539641</td>
      <td>95.203679</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Wright High School</td>
      <td>83.682222</td>
      <td>83.955000</td>
      <td>Charter</td>
      <td>1800</td>
      <td>1049400</td>
      <td>583.0</td>
      <td>93.333333</td>
      <td>96.611111</td>
      <td>94.972222</td>
    </tr>
  </tbody>
</table>
</div>




```python
top_performing_schools = merged_df.sort_values('% Overall Passing Rate', ascending=False)
top_performing_schools
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>School Name</th>
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>School Type</th>
      <th>Total Students</th>
      <th>Total School Budget</th>
      <th>Per Student Budget</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>% Overall Passing Rate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>Cabrera High School</td>
      <td>83.061895</td>
      <td>83.975780</td>
      <td>Charter</td>
      <td>1858</td>
      <td>1081356</td>
      <td>582.0</td>
      <td>94.133477</td>
      <td>97.039828</td>
      <td>95.586652</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Thomas High School</td>
      <td>83.418349</td>
      <td>83.848930</td>
      <td>Charter</td>
      <td>1635</td>
      <td>1043130</td>
      <td>638.0</td>
      <td>93.272171</td>
      <td>97.308869</td>
      <td>95.290520</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Pena High School</td>
      <td>83.839917</td>
      <td>84.044699</td>
      <td>Charter</td>
      <td>962</td>
      <td>585858</td>
      <td>609.0</td>
      <td>94.594595</td>
      <td>95.945946</td>
      <td>95.270270</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Griffin High School</td>
      <td>83.351499</td>
      <td>83.816757</td>
      <td>Charter</td>
      <td>1468</td>
      <td>917500</td>
      <td>625.0</td>
      <td>93.392371</td>
      <td>97.138965</td>
      <td>95.265668</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Wilson High School</td>
      <td>83.274201</td>
      <td>83.989488</td>
      <td>Charter</td>
      <td>2283</td>
      <td>1319574</td>
      <td>578.0</td>
      <td>93.867718</td>
      <td>96.539641</td>
      <td>95.203679</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Wright High School</td>
      <td>83.682222</td>
      <td>83.955000</td>
      <td>Charter</td>
      <td>1800</td>
      <td>1049400</td>
      <td>583.0</td>
      <td>93.333333</td>
      <td>96.611111</td>
      <td>94.972222</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Shelton High School</td>
      <td>83.359455</td>
      <td>83.725724</td>
      <td>Charter</td>
      <td>1761</td>
      <td>1056600</td>
      <td>600.0</td>
      <td>93.867121</td>
      <td>95.854628</td>
      <td>94.860875</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Holden High School</td>
      <td>83.803279</td>
      <td>83.814988</td>
      <td>Charter</td>
      <td>427</td>
      <td>248087</td>
      <td>581.0</td>
      <td>92.505855</td>
      <td>96.252927</td>
      <td>94.379391</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Bailey High School</td>
      <td>77.048432</td>
      <td>81.033963</td>
      <td>District</td>
      <td>4976</td>
      <td>3124928</td>
      <td>628.0</td>
      <td>66.680064</td>
      <td>81.933280</td>
      <td>74.306672</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Hernandez High School</td>
      <td>77.289752</td>
      <td>80.934412</td>
      <td>District</td>
      <td>4635</td>
      <td>3022020</td>
      <td>652.0</td>
      <td>66.752967</td>
      <td>80.862999</td>
      <td>73.807983</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Ford High School</td>
      <td>77.102592</td>
      <td>80.746258</td>
      <td>District</td>
      <td>2739</td>
      <td>1763916</td>
      <td>644.0</td>
      <td>68.309602</td>
      <td>79.299014</td>
      <td>73.804308</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Johnson High School</td>
      <td>77.072464</td>
      <td>80.966394</td>
      <td>District</td>
      <td>4761</td>
      <td>3094650</td>
      <td>650.0</td>
      <td>66.057551</td>
      <td>81.222432</td>
      <td>73.639992</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Huang High School</td>
      <td>76.629414</td>
      <td>81.182722</td>
      <td>District</td>
      <td>2917</td>
      <td>1910635</td>
      <td>655.0</td>
      <td>65.683922</td>
      <td>81.316421</td>
      <td>73.500171</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Figueroa High School</td>
      <td>76.711767</td>
      <td>81.158020</td>
      <td>District</td>
      <td>2949</td>
      <td>1884411</td>
      <td>639.0</td>
      <td>65.988471</td>
      <td>80.739234</td>
      <td>73.363852</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Rodriguez High School</td>
      <td>76.842711</td>
      <td>80.744686</td>
      <td>District</td>
      <td>3999</td>
      <td>2547363</td>
      <td>637.0</td>
      <td>66.366592</td>
      <td>80.220055</td>
      <td>73.293323</td>
    </tr>
  </tbody>
</table>
</div>




```python
bottom_performing_schools = merged_df.sort_values('% Overall Passing Rate', ascending=True)
bottom_performing_schools
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>School Name</th>
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>School Type</th>
      <th>Total Students</th>
      <th>Total School Budget</th>
      <th>Per Student Budget</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>% Overall Passing Rate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>10</th>
      <td>Rodriguez High School</td>
      <td>76.842711</td>
      <td>80.744686</td>
      <td>District</td>
      <td>3999</td>
      <td>2547363</td>
      <td>637.0</td>
      <td>66.366592</td>
      <td>80.220055</td>
      <td>73.293323</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Figueroa High School</td>
      <td>76.711767</td>
      <td>81.158020</td>
      <td>District</td>
      <td>2949</td>
      <td>1884411</td>
      <td>639.0</td>
      <td>65.988471</td>
      <td>80.739234</td>
      <td>73.363852</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Huang High School</td>
      <td>76.629414</td>
      <td>81.182722</td>
      <td>District</td>
      <td>2917</td>
      <td>1910635</td>
      <td>655.0</td>
      <td>65.683922</td>
      <td>81.316421</td>
      <td>73.500171</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Johnson High School</td>
      <td>77.072464</td>
      <td>80.966394</td>
      <td>District</td>
      <td>4761</td>
      <td>3094650</td>
      <td>650.0</td>
      <td>66.057551</td>
      <td>81.222432</td>
      <td>73.639992</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Ford High School</td>
      <td>77.102592</td>
      <td>80.746258</td>
      <td>District</td>
      <td>2739</td>
      <td>1763916</td>
      <td>644.0</td>
      <td>68.309602</td>
      <td>79.299014</td>
      <td>73.804308</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Hernandez High School</td>
      <td>77.289752</td>
      <td>80.934412</td>
      <td>District</td>
      <td>4635</td>
      <td>3022020</td>
      <td>652.0</td>
      <td>66.752967</td>
      <td>80.862999</td>
      <td>73.807983</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Bailey High School</td>
      <td>77.048432</td>
      <td>81.033963</td>
      <td>District</td>
      <td>4976</td>
      <td>3124928</td>
      <td>628.0</td>
      <td>66.680064</td>
      <td>81.933280</td>
      <td>74.306672</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Holden High School</td>
      <td>83.803279</td>
      <td>83.814988</td>
      <td>Charter</td>
      <td>427</td>
      <td>248087</td>
      <td>581.0</td>
      <td>92.505855</td>
      <td>96.252927</td>
      <td>94.379391</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Shelton High School</td>
      <td>83.359455</td>
      <td>83.725724</td>
      <td>Charter</td>
      <td>1761</td>
      <td>1056600</td>
      <td>600.0</td>
      <td>93.867121</td>
      <td>95.854628</td>
      <td>94.860875</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Wright High School</td>
      <td>83.682222</td>
      <td>83.955000</td>
      <td>Charter</td>
      <td>1800</td>
      <td>1049400</td>
      <td>583.0</td>
      <td>93.333333</td>
      <td>96.611111</td>
      <td>94.972222</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Wilson High School</td>
      <td>83.274201</td>
      <td>83.989488</td>
      <td>Charter</td>
      <td>2283</td>
      <td>1319574</td>
      <td>578.0</td>
      <td>93.867718</td>
      <td>96.539641</td>
      <td>95.203679</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Griffin High School</td>
      <td>83.351499</td>
      <td>83.816757</td>
      <td>Charter</td>
      <td>1468</td>
      <td>917500</td>
      <td>625.0</td>
      <td>93.392371</td>
      <td>97.138965</td>
      <td>95.265668</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Pena High School</td>
      <td>83.839917</td>
      <td>84.044699</td>
      <td>Charter</td>
      <td>962</td>
      <td>585858</td>
      <td>609.0</td>
      <td>94.594595</td>
      <td>95.945946</td>
      <td>95.270270</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Thomas High School</td>
      <td>83.418349</td>
      <td>83.848930</td>
      <td>Charter</td>
      <td>1635</td>
      <td>1043130</td>
      <td>638.0</td>
      <td>93.272171</td>
      <td>97.308869</td>
      <td>95.290520</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Cabrera High School</td>
      <td>83.061895</td>
      <td>83.975780</td>
      <td>Charter</td>
      <td>1858</td>
      <td>1081356</td>
      <td>582.0</td>
      <td>94.133477</td>
      <td>97.039828</td>
      <td>95.586652</td>
    </tr>
  </tbody>
</table>
</div>




```python
ninth = students.loc[students['grade'] == "9th"].groupby("school name")
tenth = students.loc[students['grade'] == "10th"].groupby("school name")
eleventh = students.loc[students['grade'] == "11th"].groupby("school name")
twelfth = students.loc[students['grade'] == "12th"].groupby("school name")

ninth_math_avg = pd.DataFrame(ninth['math_score'].mean())
tenth_math_avg = pd.DataFrame(tenth['math_score'].mean())
eleventh_math_avg = pd.DataFrame(eleventh['math_score'].mean())
twelfth_math_avg = pd.DataFrame(twelfth['math_score'].mean())

ninth_math_avg.reset_index(inplace=True)
tenth_math_avg.reset_index(inplace=True)
eleventh_math_avg.reset_index(inplace=True)
twelfth_math_avg.reset_index(inplace=True)

math_grades = pd.merge(ninth_math_avg, tenth_math_avg, on="school name", how="outer")
math_grades = pd.merge(math_grades, eleventh_math_avg, on="school name", how="outer")
math_grades = pd.merge(math_grades, twelfth_math_avg, on="school name", how="outer")
math_grades = math_grades.rename(columns = {"school name":"School Name","math_score_x" : "9th Grade", "math_score_y" : "10th Grade", "math_score_x" : "11th Grade", "math_score_y" : "12th Grade"})
math_grades
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>School Name</th>
      <th>11th Grade</th>
      <th>12th Grade</th>
      <th>11th Grade</th>
      <th>12th Grade</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Bailey High School</td>
      <td>77.083676</td>
      <td>76.996772</td>
      <td>77.515588</td>
      <td>76.492218</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Cabrera High School</td>
      <td>83.094697</td>
      <td>83.154506</td>
      <td>82.765560</td>
      <td>83.277487</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Figueroa High School</td>
      <td>76.403037</td>
      <td>76.539974</td>
      <td>76.884344</td>
      <td>77.151369</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Ford High School</td>
      <td>77.361345</td>
      <td>77.672316</td>
      <td>76.918058</td>
      <td>76.179963</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Griffin High School</td>
      <td>82.044010</td>
      <td>84.229064</td>
      <td>83.842105</td>
      <td>83.356164</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Hernandez High School</td>
      <td>77.438495</td>
      <td>77.337408</td>
      <td>77.136029</td>
      <td>77.186567</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Holden High School</td>
      <td>83.787402</td>
      <td>83.429825</td>
      <td>85.000000</td>
      <td>82.855422</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Huang High School</td>
      <td>77.027251</td>
      <td>75.908735</td>
      <td>76.446602</td>
      <td>77.225641</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Johnson High School</td>
      <td>77.187857</td>
      <td>76.691117</td>
      <td>77.491653</td>
      <td>76.863248</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Pena High School</td>
      <td>83.625455</td>
      <td>83.372000</td>
      <td>84.328125</td>
      <td>84.121547</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Rodriguez High School</td>
      <td>76.859966</td>
      <td>76.612500</td>
      <td>76.395626</td>
      <td>77.690748</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Shelton High School</td>
      <td>83.420755</td>
      <td>82.917411</td>
      <td>83.383495</td>
      <td>83.778976</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Thomas High School</td>
      <td>83.590022</td>
      <td>83.087886</td>
      <td>83.498795</td>
      <td>83.497041</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Wilson High School</td>
      <td>83.085578</td>
      <td>83.724422</td>
      <td>83.195326</td>
      <td>83.035794</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Wright High School</td>
      <td>83.264706</td>
      <td>84.010288</td>
      <td>83.836782</td>
      <td>83.644986</td>
    </tr>
  </tbody>
</table>
</div>




```python
ninth_reading_avg = pd.DataFrame(ninth['reading_score'].mean())
tenth_reading_avg = pd.DataFrame(tenth['reading_score'].mean())
eleventh_reading_avg = pd.DataFrame(eleventh['reading_score'].mean())
twelfth_reading_avg = pd.DataFrame(twelfth['reading_score'].mean())

ninth_reading_avg.reset_index(inplace=True)
tenth_reading_avg.reset_index(inplace=True)
eleventh_reading_avg.reset_index(inplace=True)
twelfth_reading_avg.reset_index(inplace=True)

reading_grades = pd.merge(ninth_reading_avg, tenth_reading_avg, on="school name", how="outer")
reading_grades = pd.merge(reading_grades, eleventh_reading_avg, on="school name", how="outer")
reading_grades = pd.merge(reading_grades, twelfth_reading_avg, on="school name", how="outer")
reading_grades = reading_grades.rename(columns = {"school name":"School Name","reading_score_x" : "9th Grade", "reading_score_y" : "10th Grade", "reading_score_x" : "11th Grade", "reading_score_y" : "12th Grade"})
reading_grades
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>School Name</th>
      <th>11th Grade</th>
      <th>12th Grade</th>
      <th>11th Grade</th>
      <th>12th Grade</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Bailey High School</td>
      <td>81.303155</td>
      <td>80.907183</td>
      <td>80.945643</td>
      <td>80.912451</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Cabrera High School</td>
      <td>83.676136</td>
      <td>84.253219</td>
      <td>83.788382</td>
      <td>84.287958</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Figueroa High School</td>
      <td>81.198598</td>
      <td>81.408912</td>
      <td>80.640339</td>
      <td>81.384863</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Ford High School</td>
      <td>80.632653</td>
      <td>81.262712</td>
      <td>80.403642</td>
      <td>80.662338</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Griffin High School</td>
      <td>83.369193</td>
      <td>83.706897</td>
      <td>84.288089</td>
      <td>84.013699</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Hernandez High School</td>
      <td>80.866860</td>
      <td>80.660147</td>
      <td>81.396140</td>
      <td>80.857143</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Holden High School</td>
      <td>83.677165</td>
      <td>83.324561</td>
      <td>83.815534</td>
      <td>84.698795</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Huang High School</td>
      <td>81.290284</td>
      <td>81.512386</td>
      <td>81.417476</td>
      <td>80.305983</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Johnson High School</td>
      <td>81.260714</td>
      <td>80.773431</td>
      <td>80.616027</td>
      <td>81.227564</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Pena High School</td>
      <td>83.807273</td>
      <td>83.612000</td>
      <td>84.335938</td>
      <td>84.591160</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Rodriguez High School</td>
      <td>80.993127</td>
      <td>80.629808</td>
      <td>80.864811</td>
      <td>80.376426</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Shelton High School</td>
      <td>84.122642</td>
      <td>83.441964</td>
      <td>84.373786</td>
      <td>82.781671</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Thomas High School</td>
      <td>83.728850</td>
      <td>84.254157</td>
      <td>83.585542</td>
      <td>83.831361</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Wilson High School</td>
      <td>83.939778</td>
      <td>84.021452</td>
      <td>83.764608</td>
      <td>84.317673</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Wright High School</td>
      <td>83.833333</td>
      <td>83.812757</td>
      <td>84.156322</td>
      <td>84.073171</td>
    </tr>
  </tbody>
</table>
</div>




```python
bins = [0, 585, 615, 645, 675]
budget_range = ["<585", "$585-615", "$615-645", "$645-675"]
avgs_by_budget = merged_df[["Average Math Score", "Average Reading Score", "% Passing Math", "% Passing Reading", "% Overall Passing Rate"]]

avgs_by_budget["Spending Ranges (per student)"] = pd.cut(merged_df["Per Student Budget"], bins, labels=budget_range)
binned_range = avgs_by_budget.groupby("Spending Ranges (per student)")
binned_range.mean()
```

    C:\Users\dh028365\AppData\Local\Continuum\anaconda3\lib\site-packages\ipykernel_launcher.py:5: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      """
    




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>% Overall Passing Rate</th>
    </tr>
    <tr>
      <th>Spending Ranges (per student)</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>&lt;585</th>
      <td>83.455399</td>
      <td>83.933814</td>
      <td>93.460096</td>
      <td>96.610877</td>
      <td>95.035486</td>
    </tr>
    <tr>
      <th>$585-615</th>
      <td>83.599686</td>
      <td>83.885211</td>
      <td>94.230858</td>
      <td>95.900287</td>
      <td>95.065572</td>
    </tr>
    <tr>
      <th>$615-645</th>
      <td>79.079225</td>
      <td>81.891436</td>
      <td>75.668212</td>
      <td>86.106569</td>
      <td>80.887391</td>
    </tr>
    <tr>
      <th>$645-675</th>
      <td>76.997210</td>
      <td>81.027843</td>
      <td>66.164813</td>
      <td>81.133951</td>
      <td>73.649382</td>
    </tr>
  </tbody>
</table>
</div>




```python
bins = [0, 1000, 2000, 5000]
total_size = ["Small (< 1000)", "Medium (1000 - 2000)", "Large (2000 - 5000)"]
avgs_by_size = merged_df[["Average Math Score", "Average Reading Score", "% Passing Math", "% Passing Reading", "% Overall Passing Rate"]]

avgs_by_size["School Size"] = pd.cut(merged_df["Total Students"], bins, labels=total_size)
binned_sizes = avgs_by_size.groupby("School Size")
binned_sizes.mean()
```

    C:\Users\dh028365\AppData\Local\Continuum\anaconda3\lib\site-packages\ipykernel_launcher.py:5: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      """
    




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>% Overall Passing Rate</th>
    </tr>
    <tr>
      <th>School Size</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Small (&lt; 1000)</th>
      <td>83.821598</td>
      <td>83.929843</td>
      <td>93.550225</td>
      <td>96.099437</td>
      <td>94.824831</td>
    </tr>
    <tr>
      <th>Medium (1000 - 2000)</th>
      <td>83.374684</td>
      <td>83.864438</td>
      <td>93.599695</td>
      <td>96.790680</td>
      <td>95.195187</td>
    </tr>
    <tr>
      <th>Large (2000 - 5000)</th>
      <td>77.746417</td>
      <td>81.344493</td>
      <td>69.963361</td>
      <td>82.766634</td>
      <td>76.364998</td>
    </tr>
  </tbody>
</table>
</div>




```python
school_type_bins["School Type"] = school_type_bins["School Type"].astype(int)
bins = [0, 1, 2]
school_types = ["Charter", "District"]
avgs_by_type = school_type_bins[["Average Math Score", "Average Reading Score", "% Passing Math", "% Passing Reading", "% Overall Passing Rate"]]
avgs_by_type["School Types"] = pd.cut(school_type_bins["School Type"], bins, labels=school_types)
binned_types = avgs_by_type.groupby("School Types")
binned_types.mean()
```

    C:\Users\dh028365\AppData\Local\Continuum\anaconda3\lib\site-packages\ipykernel_launcher.py:5: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      """
    




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>% Overall Passing Rate</th>
    </tr>
    <tr>
      <th>School Types</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Charter</th>
      <td>83.473852</td>
      <td>83.896421</td>
      <td>93.620830</td>
      <td>96.586489</td>
      <td>95.103660</td>
    </tr>
    <tr>
      <th>District</th>
      <td>76.956733</td>
      <td>80.966636</td>
      <td>66.548453</td>
      <td>80.799062</td>
      <td>73.673757</td>
    </tr>
  </tbody>
</table>
</div>



