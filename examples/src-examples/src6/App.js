function App() {
  const [count, setCount] = React.useState(0);

  function updateCount() {
    setCount(count + 1);
  }

  return (
    <div>
      <h1>{count}</h1>
      <button onClick={updateCount}>Count</button>
    </div>
  );
}

ReactDOM.render(<App />, document.querySelector('#app'));
