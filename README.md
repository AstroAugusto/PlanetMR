# PlanetMR
Clustering of the mass-radius relation for extrasolar and solar system planets.

## Background
As of this writing, astronomers have discovered 4,364 planets orbiting other stars. Known as extrasolar planets, or exoplanets for short, these bodies display a wide variety of features. Two of these features, mass and radius, are fundamental quantities that, taken together, convey information about a planet's internal composition. A scatter plot of the masses and radii of confirmed exoplanets for which both quantities are available looks like this (data from https://exoplanetarchive.ipac.caltech.edu/index.html):

![mass-radius](https://github.com/AstroAugusto/PlanetMR/blob/main/MR.png)

In this plot, the planet mass, *M*, is shown in units of one Jupiter mass, *M*<sub>Jup</sub>, and the planet radius, *R*, in units of one Jupiter radius, *R*<sub>Jup</sub>. Several studies have seeked to understand these data, and to make predictions from them. For example, to predict planet masses when only astronomical measurements of radii are available (or viceversa), Chen & Kipping (2017) used a probabilistic forecasting model, and Tasker et al. (2020) employed a deep learning framework. In addition, the Chen & Kipping model classifies the planet population according to their mass into three groups, which the authors label Terran (*M* < 2*M*<sub>E</sub>, where *M*<sub>E</sub> is one Earth mass), Neptunian (2 *M*<sub>E</sub> < *M* < 130.3 *M*<sub>E</sub>) and Jovian (130.3 *M*<sub>E</sub> < *M* < 2.66 x 10<sup>4</sup> *M*<sub>E</sub>).

These, and other 
