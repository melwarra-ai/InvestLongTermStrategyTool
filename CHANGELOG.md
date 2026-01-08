# Changelog

All notable changes to Long Term Strategy Optimizer will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [5.5.0] - 2026-01-08 - 🎯 STABLE RELEASE

### Status
- **STABLE** - Production-ready baseline version
- Based on verified working code (`LongTermIvestor_08012026_fixed.py`)
- All core features tested and functional
- Benchmark visualization confirmed working

### ✅ Verified Working
- Benchmark visualization (SPY, QQQ, VTI, IWM, DIA) fully functional
- pandas Series → Plotly data conversion working correctly
- Chart rendering displays all 3 lines (Portfolio, Goal, Benchmark)
- Asset deployment workflow complete
- Drift detection and alerts operational
- Rebalancing calculations accurate
- Database persistence stable

### 🔧 Code Quality Improvements
- Added version tracking (`VERSION`, `VERSION_DATE`, `VERSION_NAME`)
- Clean imports and organization
- Comprehensive inline documentation
- Proper error handling throughout
- Consistent code formatting

### 📝 Documentation
- Complete release notes document created
- Inline comments throughout codebase
- User-friendly UI explanations
- Detailed help expanders in all sections
- Troubleshooting guides

### 🎨 Technical Details
- Fixed pandas DataFrame/Series handling for yfinance data
- Proper list conversion for Plotly compatibility
- Correct benchmark data normalization
- Stable chart rendering

### 📦 This Release Is The Stable Baseline For Future Development
- All v5.x features consolidated
- Clean, maintainable codebase
- Ready for production use
- Foundation for v5.6+ enhancements

---

## [5.0.0] - 2026-01-05

### 🎨 Changed (Branding)
- **Application name**: Changed from "AlphaStream Wealth Master" to "Long Term Strategy Optimizer"
- **Sidebar title**: Updated to "Portfolio Optimizer"
- **Footer**: Updated to show v5.0 and new name
- **Page title**: Browser tab now shows new name

### ✨ Enhanced (Chart Visualization)
- **Benchmark line visibility**: Increased line width from 2.5px to 4px
- **Benchmark line style**: Changed from dash-dot to dotted for better visibility
- **Benchmark line color**: Changed to bright orange-red (#ff4500) for maximum contrast
- **Chart title**: Removed redundant title to eliminate overlapping with legend
- **Legend position**: Moved below chart (y=-0.15) to prevent overlap
- **Portfolio fill**: Removed area fill to ensure benchmark visibility
- **Chart height**: Adjusted to 550px for optimal display
- **Margins**: Optimized for cleaner layout (t=20, b=80)

### 📝 Improved (Documentation)
- **Chart explanation**: Enhanced documentation about benchmark assumptions
- **Hover tooltips**: Clarified benchmark shows "100% invested at start"
- **User guidance**: Added more context about benchmark comparison

### 🐛 Fixed
- Fixed benchmark line not visible on chart (covered by portfolio fill)
- Fixed chart title overlapping with legend
- Fixed messy layout with overlapping elements

---

## [4.0.0] - 2025-12-XX (AlphaStream Era)

### ✨ Added
- Multi-portfolio management system
- Intelligent drift detection with customizable tolerance
- One-click rebalancing execution
- Rebalancing history tracking
- Benchmark comparison feature
- Performance vs Goal Path chart
- Global dashboard with portfolio tiles
- Asset deployment tracking (0-100%)
- Recently rebalanced indicators (24-hour cooldown)

### 🎨 Enhanced
- Professional fintech styling
- Color-coded status indicators
- Real-time portfolio valuation
- Multi-currency support (USD/CAD)

### 🐛 Known Issues
- Benchmark line hard to see on chart (fixed in v5.0)
- Chart title overlapping with legend (fixed in v5.0)

---

## [3.0.0] - 2025-XX-XX

### ✨ Added
- Rebalancing functionality
- Drift alerts and warnings
- Asset allocation monitoring

### 🎨 Enhanced
- Improved UI/UX
- Better data visualization

---

## [2.0.0] - 2025-XX-XX

### ✨ Added
- Portfolio performance tracking
- Goal path visualization
- Historical data storage

---

## [1.0.0] - 2025-XX-XX

### ✨ Initial Release
- Basic portfolio management
- Asset tracking
- Simple allocation display
- Yahoo Finance integration

---

## Release Notes Format

Each version includes:
- **🎨 Changed**: Modifications to existing features
- **✨ Added**: New features
- **🐛 Fixed**: Bug fixes
- **📝 Improved**: Enhancements to existing features
- **🗑️ Removed**: Deprecated features
- **⚠️ Security**: Security-related changes

---

## Version Numbering

**Format:** MAJOR.MINOR.PATCH

- **MAJOR**: Breaking changes or major redesign
- **MINOR**: New features, backwards compatible
- **PATCH**: Bug fixes, minor improvements

**Current Version:** 5.0.0

---

## Migration Guides

### From v4.0 to v5.0
- ✅ **No breaking changes**
- ✅ **No data migration needed**
- ✅ **Backward compatible**
- Simply replace the file and run
- All existing portfolios work immediately

### From v3.0 to v4.0
- Added drift detection features
- Added rebalancing history
- May need to set drift tolerance in existing profiles

### From v2.0 to v3.0
- Added deployment tracking
- May need to update asset data structure

---

## Upcoming Features (Roadmap)

### Planned for v5.1
- [ ] Export portfolio data to CSV
- [ ] Email alerts for drift detection
- [ ] Custom benchmark portfolios
- [ ] Tax lot tracking

### Planned for v6.0
- [ ] Multi-benchmark comparison
- [ ] Risk metrics (Sharpe ratio, volatility)
- [ ] Sector allocation analysis
- [ ] Dividend tracking
- [ ] Mobile-responsive improvements

### Under Consideration
- [ ] Dark mode theme
- [ ] Chart export as image
- [ ] PDF report generation
- [ ] Integration with brokerage APIs
- [ ] Automated rebalancing suggestions

---

## Support & Feedback

Found a bug? Have a feature request?

1. Check existing documentation
2. Review troubleshooting guide
3. Verify you're on the latest version
4. Document the issue with screenshots

---

## Credits

**v5.0 Development Team:**
- Chart visualization improvements
- UX/UI enhancements
- Documentation updates

**v4.0 Development Team:**
- Core rebalancing engine
- Drift detection system
- Multi-portfolio framework

**Special Thanks:**
- Streamlit community
- Yahoo Finance (yfinance) contributors
- Beta testers and early adopters

---

**Last Updated:** January 5, 2026  
**Current Version:** 5.0.0  
**Status:** Production Ready ✅
