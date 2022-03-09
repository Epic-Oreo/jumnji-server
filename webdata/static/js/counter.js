
// DOM Element's
const counters = document.querySelectorAll('.counter');

/*** Using forEach() 

/*** Same functionality, now using for...of ***/

for(let n of counters) {
    const updateCount = () => {
        const target = + n.getAttribute('data-target');
        const count = + n.innerText;
        const speed = 5000;

        let tmp;
        const inc = target / speed; 

        if(count < target) {
            tmp = Math.ceil(count + inc)
            n.innerText = tmp;
            setTimeout(updateCount, 1);
        } else {
            n.innerText = target;
        }
    }

    updateCount();
}


