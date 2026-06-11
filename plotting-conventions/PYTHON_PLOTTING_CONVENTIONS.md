# Python Plotting Conventions

## Figure setup template

```python
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# single-column: figsize=(3.25, 2.2); double-column: figsize=(7.0, 2.2)
fig = plt.figure(1, figsize=(3.25, 2.2))

plt.rc('font', family='serif')
plt.rc('text', usetex=False)  # set True for final publication output
plt.rc('xtick', top=True, direction='out', labelsize=7)
plt.rc('ytick', right=True, direction='out', labelsize=7)
plt.rc('axes', labelsize=8)
plt.rc('legend', handlelength=4.0)

nrow_fig = 1
ncol_fig = 1
gs = plt.GridSpec(nrow_fig, ncol_fig)
gs.update(wspace=0.25, hspace=0.35)

axs = np.empty((nrow_fig, ncol_fig), dtype=object)
for j in range(ncol_fig):
    for i in range(nrow_fig):
        axs[i,j] = plt.subplot(gs[i,j])
        axs[i,j].minorticks_on()

# manual positioning — minimize whitespace
axleft = 0.18; axbottom = 0.16; axright = 0.96; axtop = 0.92
fig.subplots_adjust(left=axleft, bottom=axbottom, right=axright, top=axtop)
```

Adjust `nrow_fig`, `ncol_fig`, and `figsize` as needed for multi-panel figures.

## Style rules

- **Figure API**: always use `ax.plot()`, `ax.set_xlabel()`, etc. — never `plt.plot()`
- **Figure widths**: single-column = 3.25in, double-column = 7.0in
- **Ticks**: all four sides on, minor ticks on, direction outward
- **No clutter**: no titles, no grid, no text annotations, `frameon=False` on legends
- **Tight bounds manually**: set `xlim`/`ylim` tightly to verified min/max data ranges — no unnecessary whitespace
- **Manual positioning**: use `fig.subplots_adjust()` to control margins; no `tight_layout`
- **Colors**: always use default matplotlib cycle colors (`C0`, `C1`, `C2`, ...)
- **Lines**: plain lines only, `linewidth=1` (use `0.8` for dense data); no markers
- **Axis labels**: format as `Quantity name $symbol~(\mathrm{units})$`
  - e.g., `r"Velocity $v_\mathrm{c}~(\mathrm{cm}\,\mathrm{s}^{-1})$"`
  - e.g., `r"Position $x~(\mathrm{cm})$"`
- **Saving**: save as a pdf format; filename = `<script_name>_<suffix>.pdf`
  ```python
  plt.savefig('scriptname_suffix.pdf')
  ```


## Colorbars

- Use colormap `turbo` as the default colormap for qualitative color ranges. 
- For divergent values (negative and positive values) use `RdBu` as the default.

Use `matplotlib.colorbar.ColorbarBase` with manually positioned axes:

```python
norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
cmap = matplotlib.colormaps['turbo_r']

# map values to colors: col = cmap(norm(x))

# manually position colorbar axis
axleft   = 0.15
axright  = 0.97
axtop    = 0.82
axwidth  = axright - axleft
axheight = (axtop - 0.15) * 0.03
axpad    = 0.02
cax = fig.add_axes([axleft, axtop + axpad, axwidth, axheight])

cb = matplotlib.colorbar.ColorbarBase(
    cax, cmap=cmap, norm=norm,
    orientation='horizontal', ticklocation='top')
cb.set_label(r'label')
```

Adjust positioning and `orientation` to match layout. Use `LogNorm` for log-scaled colorbars.
