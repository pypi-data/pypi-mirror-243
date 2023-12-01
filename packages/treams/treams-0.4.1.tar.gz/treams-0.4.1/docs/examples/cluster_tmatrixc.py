import matplotlib.pyplot as plt
import numpy as np

import treams

k0 = 2 * np.pi / 700
materials = [treams.Material(-16.5 + 1j), treams.Material()]
lmax = mmax = 3
radii = [65, 55]
positions = [[-40, -50, 0], [40, 50, 0]]
lattice = treams.Lattice(300)
kz = 0.005

sphere = treams.TMatrix.sphere(lmax, k0, radii[0], materials)
chain = sphere.latticeinteraction.solve(lattice, kz)
bmax = 3.1 * lattice.reciprocal
cwb = treams.CylindricalWaveBasis.diffr_orders(kz, mmax, lattice, bmax)
chain_tmc = treams.TMatrixC.from_array(chain, cwb)

cylinder = treams.TMatrixC.cylinder(np.unique(cwb.kz), mmax, k0, radii[1], materials)

cluster = treams.TMatrixC.cluster([chain_tmc, cylinder], positions).interaction.solve()
inc = treams.plane_wave(
    [np.sqrt(k0 ** 2 - kz ** 2), 0, kz],
    [np.sqrt(0.5), np.sqrt(0.5)],
    k0=chain.k0,
    material=chain.material,
)
sca = cluster @ inc.expand(cluster.basis)

grid = (
    np.mgrid[-300:300:61j, 0:1, -150:150:31j].squeeze().transpose((1, 2, 0))[:, :-1, :]
)
ez = np.zeros_like(grid[..., 0], complex)
valid = cluster.valid_points(grid, radii)
ez[valid] = (inc.efield(grid[valid]) + sca.efield(grid[valid]))[..., 2]

ez = np.concatenate(
    (
        np.real(ez.T * np.exp(-1j * kz * lattice[...])),
        ez.T.real,
        np.real(ez.T * np.exp(1j * kz * lattice[...])),
    )
)
zaxis = np.concatenate((grid[0, :, 2] - 300, grid[0, :, 2], grid[0, :, 2] + 300,))

fig, ax = plt.subplots(figsize=(10, 20))
pcm = ax.pcolormesh(grid[:, 0, 0], zaxis, ez, shading="nearest", vmin=-1, vmax=1,)
cb = plt.colorbar(pcm)
cb.set_label("$E_z$")
ax.set_xlabel("x (nm)")
ax.set_ylabel("z (nm)")
ax.set_aspect("equal")
fig.show()
