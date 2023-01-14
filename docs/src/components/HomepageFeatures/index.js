import React from "react";
import clsx from "clsx";
import styles from "./styles.module.css";

const FeatureList = [
  {
    title: "Deux mode de lancement",
    png: require("@site/static/img/rocket.jpg").default,
    description: (
      <>
        Notre Application peut être lancée avec une IHM ou directement en ligne
        de commandes avec un mode verbose
      </>
    ),
  },
  {
    title: "Deux mode d'exécution",
    png: require("@site/static/img/ihm.jpg").default,
    description: (
      <>
        Pour résoudre le calcul de l'état N+1, notre application propose deux
        modes de calcul, multi-threading sans barrière de synchronisation et
        avec barrière de synchronisation
      </>
    ),
  },
  {
    title: "Création de carte",
    png: require("@site/static/img/drawing.jpg").default,
    description: (
      <>
        Notre application offre la possibilité à l'utilisateur de créer ses
        propres cartes
      </>
    ),
  },
];

function Feature({ Svg, title, description, png }) {
  return (
    <div className={clsx("col col--4")}>
      <div className="text--center">
        {Svg && <Svg className={styles.featureSvg} role="img" />}
        {png && <img src={png} height="300" />}
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
