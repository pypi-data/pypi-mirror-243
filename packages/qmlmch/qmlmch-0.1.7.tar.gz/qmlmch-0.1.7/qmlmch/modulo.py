import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.special import sph_harm
import numpy as np
from scipy.special import assoc_laguerre


class hydrogen_atom(object):
    """
    Esta clase permite graficar los orbitales atómicos complejos, imaginarios y reales del átomo de hidrógeno en 3D.
    Además, permite graficar la densidad de probabilidad en 3D.

    Parámetros
    ----------
    n : int
        Número cuántico principal
    l : int
        Número cuántico orbital
    m : int
        Número cuántico magnético
    a : float
        Radio de Bohr
    num_points : int
        Número de puntos para generar la malla de coordenadas esféricas

    Metodos relevantes
    ------------------
    radial_wavefunction(r)
        Calcula la función de onda radial para un valor de radio dado.

    angular_wavefunction(theta, phi)
        Calcula la función de onda angular para un valor de theta y phi dados.

    wave_function(r, theta, phi)
        Calcula la función de onda para un valor de r, theta y phi dados.

    angular_graph()
        Grafica la función de onda angular en 3D.
        Tanto la parte compleja,imaginaria y real.

    Real_graph()
        Grafica la función de onda real en 3D.

    Density_probability_graph()
        Grafica de densidad de probabilidad en 3D.

    """

    def __init__(self, n, l, m):
        """
        Inicializa los parámetros de la clase.
        """
        self.n = n
        self.l = l
        self.m = m
        self.a = 1 # En unidades atómicas
        self.num_points = 200
        theta_vals = np.linspace(0, np.pi, self.num_points)
        phi_vals = np.linspace(0, 2 * np.pi, self.num_points)
        self.Theta, self.Phi = np.meshgrid(theta_vals, phi_vals)
        self.check_validity(n, l, m)

    def check_validity(self, n, l, m):
        """
        Esta función verifica que los valores de n, l y m sean válidos.

        Parámetros
        ----------
        n : int
            Número cuántico principal
        l : int
            Número cuántico orbital
        m : int
            Número cuántico magnético

        Excepciones
        -----------
        ValueError
            Si n < 1
            Si l >= n
            Si |m| > l
            Si (n - l - 1) < 0
            Si (n + l) < 0
            Si l < 0
        """

        if n < 1:
            raise ValueError('El número cuántico principal debe ser mayor o igual a 1.')
        if l >= n:
            raise ValueError('El número cuántico orbital debe ser menor que el número cuántico principal.')
        if np.abs(m) > l:
            raise ValueError('El número cuántico magnético debe ser menor o igual al número cuántico orbital.')
        if (n - l - 1) < 0:
            raise ValueError('El número cuántico principal debe ser mayor o igual al número cuántico orbital más uno.')
        if (n + l) < 0:
            raise ValueError('El número cuántico principal debe ser mayor o igual al número cuántico orbital.')
        if l < 0:
            raise ValueError('El número cuántico orbital debe ser mayor o igual a cero.')




    def radial_wavefunction(self, r):
        """
        Esta función calcula la función de onda radial para un valor de radio dado.

        Parámetros
        ----------
        r : float
            Radio en unidades atómicas

        Devuelve
        -------
        float
            Valor de la función de onda radial para el radio dado.
        """
        n = self.n
        l = self.l
        a = self.a

        rho = (2 * r) / (n*a)
        L = assoc_laguerre(rho, n-l-1, 2*l + 1)
        R = np.exp(-rho / 2) * rho ** l * L
        fact = np.sqrt((2 / (n * a)) ** 3 * np.math.factorial(n - l - 1) / (2 * n * np.math.factorial(n + l)))
        return fact * R

    def angular_wavefunction(self, theta, phi):
        """
        Esta función calcula la función de onda angular para un valor de theta y phi dados.

        Parámetros
        ----------
        theta : float
            Ángulo theta en radianes
        phi : float
            Ángulo phi en radianes

        Devuelve
        -------
        float
            Valor de la función de onda angular para los valores de theta y phi dados.
        """
        m = self.m
        l = self.l
        return sph_harm(m, l, phi, theta)

    def wave_function(self, r, theta, phi):
        """
        Esta función calcula la función de onda para un valor de r, theta y phi dados.

        Parámetros
        ----------
        r : float
            Radio en unidades atómicas
        theta : float
            Ángulo theta en radianes
        phi : float
            Ángulo phi en radianes

        Devuelve
        -------
        float
            Valor de la función de onda para los valores de r, theta y phi dados.
        """
        return self.radial_wavefunction(r) * self.angular_wavefunction(theta, phi)

    def sph2cart(self,r,theta,phi):
        """
        Este método convierte coordenadas esféricas en coordenadas cartesianas.

        Parámetros
        ----------
        r : float
            Radio en unidades atómicas
        theta : float
            Ángulo theta en radianes
        phi : float
            Ángulo phi en radianes

        Devuelve
        -------
        float
            Valores de coordenadas cartesianas para los valores de r, theta y phi dados.
        """
        x = r*np.sin(theta)*np.cos(phi)
        y = r*np.sin(theta)*np.sin(phi)
        z = r*np.cos(theta)
        return (x,y,z)

    def RDF(self, r):
        """
        Este método calcula la función de distribución radial (RDF) para un valor de radio dado.

        Parámetros
        ----------
        r : float
            Radio en unidades atómicas

        Devuelve
        -------
        float
            Valor de la RDF para el radio dado.
        """
        return 4 * np.pi * r**2 * self.radial_wavefunction(r)**2

    def probability_density(self, r, theta, phi):
        """
        Este método calcula la probabilidad de densidad para un valor de r, theta y phi dados.

        Parámetros
        ----------
        r : float
            Radio en unidades atómicas
        theta : float
            Ángulo theta en radianes
        phi : float
            Ángulo phi en radianes

        Devuelve
        -------
        float
            Valor de la probabilidad de densidad para los valores de r, theta y phi dados.
        """
        return np.abs(self.wave_function(r, theta, phi)) ** 2

    # Crea una función de distribución acumulada (CDF)
    def cumulative_distribution_function(self, r_values):
        """
        ESte método crea una función de distribución acumulada (CDF) para un conjunto de valores de radio dados.

        Parámetros
        ----------
        r_values : array_like
            Valores de radio en unidades atómicas

        Devuelve
        -------
        array_like
            Valores de la CDF para los valores de radio dados.
        """
        cdf = np.zeros_like(r_values)
        for i, _ in enumerate(r_values):
            cdf[i] = np.trapz([self.RDF(val) for val in r_values[:i+1]], r_values[:i+1])
        return cdf

    def angular_graph(self):
        """
        Esta función grafica la función de onda angular en 3D para la parte compleja, imaginaria y real.
        """
        Theta = self.Theta
        Phi = self.Phi
        n = self.n
        l = self.l
        m = self.m
        r = self.a

        if self.m == 0:
            # cargar datos para x, y, z
            x,y,z = self.sph2cart(np.abs(self.wave_function(r,Theta, Phi)), Theta, Phi)
            titulo = [f'n={n},l={l},m={m}<br>Complex']

            #creamos la figura
            fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])

            #agregamos el subtitulo
            fig.update_layout(annotations=[
                dict(x=0.5, y=-0.1, xref="paper", yref="paper", showarrow=False, text=titulo[0], font=dict(size=20))
            ])

            # Agregar colorbar
            fig.update_layout(scene=dict(
                                xaxis_title='x',
                                yaxis_title='y',
                                zaxis_title='z'))

            # Ajustar el tamaño de la fuente en el título
            fig.update_layout(title_text=f'<b>Three-dimensional angular graph with set of quantum number (n={n}, l={l}, m={m})<b>',
                              title_font=dict(size=25))

            #plotly.offline.iplot(fig)
            fig.show()

        else:
            # Cargar datos para x, y, z
            x2, y2, z2 = self.sph2cart(np.abs(np.imag(self.wave_function(r,Theta, Phi))), Theta, Phi)
            x3, y3, z3 = self.sph2cart(np.abs(np.real(self.wave_function(r,Theta, Phi))), Theta, Phi)
            x1, y1, z1 = self.sph2cart(np.abs(self.wave_function(r, Theta, Phi)), Theta, Phi)

            # Crear una figura con subgráficas organizadas en filas y columnas
            titulos = [
                f'n={n},l={l},m=\u00B1{m}<br>Complex',
                f'n={n},l={l},m=\u00B1{m}<br>Imageninary',
                f'n={n},l={l},m=\u00B1{m}<br>Real'
            ]

            # Crear subgráficos en 3D
            fig = make_subplots(rows=1, cols=3, subplot_titles=titulos,
                                specs=[[{'type': 'surface'}, {'type': 'surface'}, {'type': 'surface'}]])

            # Añadir trama de superficie a la figura
            fig.add_trace(go.Surface(z=z1, x=x1, y=y1), row=1, col=1)
            fig.add_trace(go.Surface(z=z2, x=x2, y=y2), row=1, col=2)
            fig.add_trace(go.Surface(z=z3, x=x3, y=y3), row=1, col=3)

            # Configurar el diseño de la figura
            fig.update_layout(scene=dict(
                                xaxis_title='x',
                                yaxis_title='y',
                                zaxis_title='z'))


            # Ajustar el tamaño de la fuente en el título
            fig.update_layout(title_text=f'<b>Three-dimensional angular graph with set of quantum number (n={n}, l={l}, m={m})<b>',
                              title_font=dict(size=25))

            # Añadir título a través de annotations
            fig.update_layout(annotations=[
                dict(x=0.15, y=-0.1, xref="paper", yref="paper", showarrow=False, text=titulos[0], font=dict(size=20)),
                dict(x=0.5, y=-0.1, xref="paper", yref="paper", showarrow=False, text=titulos[1], font=dict(size=20)),
                dict(x=0.85, y=-0.1, xref="paper", yref="paper", showarrow=False, text=titulos[2], font=dict(size=20)),
            ])

            #guardar la figura

            fig.show()


    def Real_graph(self):
        """
        Esta función grafica la función de onda real en 3D para todos los valores de l < n.
        """
        Theta = self.Theta
        Phi = self.Phi
        n = self.n
        l = self.l
        m = self.m
        r = self.a

        #cramos una figura con subgráficas organizadas en filas y columnas
        fig = make_subplots(rows=int(np.ceil(n/3)), cols=3,
                            subplot_titles=[f'Real<br>n={n}, l={i}, m={m} ' for i in range(n)],
                            specs=[[{'type': 'surface'}, {'type': 'surface'}, {'type': 'surface'}] for _ in range(int(np.ceil(n/3)))],
                            horizontal_spacing=0.1, vertical_spacing=0.15)

        # Ajustar el tamaño de la figura global
        fig.update_layout(width=1000, height=1000)

        # Ajustar el tamaño de la fuente en el título
        quantum_number_l = [i for i in range(n)]
        fig.update_layout(title_text=f'<b>Three-dimensional angular graph with set of quantum number (n={n}, l={quantum_number_l}, m={m})<b>',
                              title_font=dict(size=20))

        # Añadir superficies con diferentes conjuntos de datos a cada subgráfico
        for i in range(self.n):
            self.l = i
            x1, y1, z1 = self.sph2cart(np.abs(self.wave_function(r, Theta, Phi)), Theta, Phi)

            # Añadir trama de superficie a la subgráfica individual
            surf = go.Surface(z=z1, x=x1, y=y1, showscale=False)
            fig.add_trace(surf, row=i//3 + 1, col=i%3 + 1)

            #Quitamos la barra de color
            surf.update(colorbar=dict(thickness=0, ticklen=0))

            # Configurar el diseño de la subgráfica
            fig.update_layout(scene=dict(
                                xaxis_title='x',
                                yaxis_title='y',
                                zaxis_title='z'))

        # Mostrar la gráfica interactivo
        fig.show()



    def Density_probability_graph(self, num_points=5000):
        """
        Esta función grafica la densidad de probabilidad en 3D.
        """


        n = self.n
        l = self.l
        m = self.m
        r = self.a
        num_points = num_points

        Theta    = np.random.uniform(0, np.pi, num_points)
        Phi      = np.random.uniform(0, 2 * np.pi, num_points)
        r_vals = np.linspace(0, 30, num_points)
        cdf_values = self.cumulative_distribution_function(r_vals)

        # Normaliza la CDF para que esté entre 0 y 1
        cdf_values /= cdf_values.max()

        # Genera valores de r ponderados según la RDF
        random_numbers = np.random.rand(num_points)
        r = np.interp(random_numbers, cdf_values, r_vals)

        # Calculamos la probabilidad de densidad
        #prob_density = self.probability_density(r, Theta, Phi)

        prob_density = (np.abs(self.wave_function(r, Theta, Phi)))**2
        x = r * np.sin(Theta) * np.cos(Phi)
        y = r * np.sin(Theta) * np.sin(Phi)
        z = r * np.cos(Theta)

        #utilizamos flatten para convertir los arreglos en vectores para poder graficarlos en 3D
        prob_density_normalized = (prob_density - prob_density.min()) / (prob_density.max() - prob_density.min())
        fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z, mode='markers',
                                                marker=dict(size=2, opacity=1, color=prob_density_normalized, colorscale='Viridis'))])
        #Invetimos la escala de colores para que se vea mejor
        fig.update_layout(scene = dict(
                            xaxis_title='x',
                            yaxis_title='y',
                            zaxis_title='z'),coloraxis_colorbar=dict(
                title="Probabilidad"))

        fig.update_layout(scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'))
        fig.update_traces(marker=dict(colorbar=dict(title='Probabilidad', tickformat=".0%")))

        fig.update_layout(title_text=f'<b>Density probability (\u007C \u03C8 \u007C²) for n={n}, l={l}, m={m}</b> ',
                        title_font=dict(size=25))
        fig.show()

    
