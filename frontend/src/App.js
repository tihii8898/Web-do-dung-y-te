import { Container } from 'react-bootstrap'


import Header from './components/Header';
import Footer from './components/Footer';



function App() {
  return (
    <div className="App">
      <Header/>
      <main className='py-5'>
        <Container>
          <h1>Ố là là la</h1>
        </Container>
      </main>
      <Footer/>
    </div>
  );
}

export default App;
