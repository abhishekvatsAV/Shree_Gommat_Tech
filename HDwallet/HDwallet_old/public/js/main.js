function generate_seed() {
  //creates new seed
  var new_seed = lightwallet.keystore.generateRandomSeed(); //creating 12 word

  document.getElementById("seed").value = new_seed;

  generate_addresses(new_seed); //sending the 12 word to make them private key
}

var totalAddresses = 0;
var direvationPath = "";

function generate_addresses(seed) {
  //creating addresses by the seed (12 words )
  if (seed == undefined) {
    //if there is no seed
    seed = document.getElementById("seed").value; //taking the value from the textbox
  }

  if (!lightwallet.keystore.isSeedValid(seed)) {
    //if the seed is not legal or incorrect
    document.getElementById("info").innerHTML = "Please enter a valid seed";
    return;
  }

  totalAddresses = prompt("How many addresses do you want to generate"); //number of adresses

  if (!Number.isInteger(parseInt(totalAddresses))) {
    //checking the input that was entered
    document.getElementById("info").innerHTML = "Please enter valid number of addresses";
    return;
  }

  var password = Math.random().toString(); //creating random password

  lightwallet.keystore.createVault(
    {
      password: password,
      seedPhrase: seed,
    },
    function (err, ks) {
      ks.keyFromPassword(password, function (err, pwDerivedKey) {
        if (err) {
          document.getElementById("info").innerHTML = err;
        } else {
          ks.generateNewAddress(pwDerivedKey, totalAddresses);
          var addresses = ks.getAddresses(); //getting the adresses in array from the keystore

          var web3 = new Web3(new Web3.providers.HttpProvider("https://ropsten.infura.io/v3/3fb8dd7c991d45ada6420c1b4280a121")); //Direvation path here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
          var html = "";

          for (
            var count = 0;
            count < addresses.length;
            count++ //for each adress in the addresses
          ) {
            var address = addresses[count]; //getting the addresses
            var private_key = ks.exportPrivateKey(address, pwDerivedKey); //returns private key of the address
            var balance = web3.eth.getBalance("0x" + address); //sending the address as parameter to get its balance

            html = html + "<li>"; //showing the information on the screen about address its private key and its balance
            html = html + "<p><b>Address: </b>0x" + address + "</p>";
            html = html + "<p><b>Private Key: </b>0x" + private_key + "</p>"; //its private
            html = html + "<p><b>Balance: </b>" + web3.fromWei(balance, "ether") + " ethereum</p>"; //its balance
            html = html + "</li>";
          }

          document.getElementById("list").innerHTML = html; //all of this inside a list
        }
      });
    }
  );
}

function send_ether() {
  //this function makes signed transaction between accounts..
  //only if the 12 word are entered into the info textbox the owner of can send by simply
  //chooce the from: adress(not private key because 12 words secret phrase are already entered) and to: (adress ofcourse)
  //
  var seed = document.getElementById("seed").value;

  if (!lightwallet.keystore.isSeedValid(seed)) {
    //checking if the seed
    document.getElementById("info").innerHTML = "Please enter a valid seed";
    return;
  }

  var password = Math.random().toString();

  lightwallet.keystore.createVault(
    {
      password: password,
      seedPhrase: seed,
    },
    function (err, ks) {
      ks.keyFromPassword(password, function (err, pwDerivedKey) {
        if (err) {
          document.getElementById("info").innerHTML = err;
        } else {
          ks.generateNewAddress(pwDerivedKey, totalAddresses);

          ks.passwordProvider = function (callback) {
            callback(null, password);
          };
          var provider = new HookedWeb3Provider({
            host: "https://ropsten.infura.io/v3/3fb8dd7c991d45ada6420c1b4280a121",
            transaction_signer: ks,
          });

          var web3 = new Web3(provider);

          var from = document.getElementById("address1").value;
          var to = document.getElementById("address2").value;
          var value = web3.toWei(document.getElementById("ether").value, "ether");
          web3.eth.sendTransaction(
            {
              from: from,
              to: to,
              gasLimit: "0xC350",
              gasPrice: "80000000000",
              value: value,
              gas: "21000",
            },
            function (error, result) {
              if (error) {
                document.getElementById("info").innerHTML = error;
              } else {
                document.getElementById("info").innerHTML = "Txn hash: " + result;
              }
            }
          );
        }
      });
    }
  );
}
