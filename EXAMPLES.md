0. Create initial claude.md file manually.
1. Read the file, outline it's structure and write in a markdown file under 'docs/'.
2. update the claude.md file
3. initialize the project using uv and git, install the required packages.
4. Create an interactive data visualization dashboard using the sample data provided in `Financial_Sample.xlsx`. The dashboard should allow users to explore the financial data through various charts, graphs, filters, ranges, etc.
------------------

- fix streamlit warnings
- add testcases
- plan: dark mode feature. user should be able to toggle dark mode on/off.
- chagne date range from slidebar to date picker.
- skill: streamlit skill
- subagent: docer expert in writing docs
- hook: dot env protector
- mcp: 
    - custom: financial-data server. claude query Financial_Sample.xlsx directly instead of writing a one-off script each time. 
    - public: playwright mcp lets claude open and use the running dashboard in a real browsedr
- github: issue implementation, auto pr review 
- workflow automation