document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generateBtn');
    const ingredientsInput = document.getElementById('ingredients');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const recipeResult = document.getElementById('recipeResult');
    const videoContainer = document.getElementById('videoContainer');
    
    generateBtn.addEventListener('click', async () => {
        const ingredients = ingredientsInput.value.trim();
        
        if (!ingredients) {
            alert('Please enter some ingredients!');
            return;
        }

        // Show loading state
        loadingIndicator.classList.remove('hidden');
        recipeResult.classList.add('hidden');
        generateBtn.disabled = true;
        generateBtn.classList.add('opacity-50', 'cursor-not-allowed');

        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ ingredients }),
            });

            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Failed to generate recipe');
            }

            // Update UI with recipe
            document.getElementById('recipeName').textContent = data.name;
            document.getElementById('cookingTime').textContent = data.cookingTime;
            
            // Update ingredients list
            const ingredientsList = document.getElementById('ingredientsList');
            ingredientsList.innerHTML = '';
            data.ingredients.forEach(ingredient => {
                const li = document.createElement('li');
                li.textContent = ingredient;
                ingredientsList.appendChild(li);
            });
            
            // Update instructions list
            const instructionsList = document.getElementById('instructionsList');
            instructionsList.innerHTML = '';
            data.instructions.forEach(instruction => {
                const li = document.createElement('li');
                li.textContent = instruction;
                instructionsList.appendChild(li);
            });
            
            // Update nutritional info
            document.getElementById('nutritionalInfo').textContent = data.nutritionalInfo;
            
            // Search for related videos
            await searchAndDisplayVideos(data.name);
            
            // Show the recipe
            recipeResult.classList.remove('hidden');
            recipeResult.scrollIntoView({ behavior: 'smooth' });
            
        } catch (error) {
            alert(error.message || 'Failed to generate recipe. Please try again.');
            console.error('Error:', error);
        } finally {
            // Reset UI state
            loadingIndicator.classList.add('hidden');
            generateBtn.disabled = false;
            generateBtn.classList.remove('opacity-50', 'cursor-not-allowed');
        }
    });

    async function searchAndDisplayVideos(recipeName) {
        try {
            const response = await fetch(`/api/videos?recipe=${encodeURIComponent(recipeName)}`);
            const videos = await response.json();
            
            videoContainer.innerHTML = '';
            
            videos.forEach(video => {
                const videoCard = document.createElement('div');
                videoCard.className = 'bg-gray-50 rounded-lg overflow-hidden shadow-md transition-transform hover:scale-105';
                videoCard.innerHTML = `
                    <div class="aspect-w-16 aspect-h-9">
                        <iframe 
                            src="https://www.youtube.com/embed/${video.videoId}"
                            class="w-full h-64 object-cover"
                            frameborder="0"
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                            allowfullscreen>
                        </iframe>
                    </div>
                    <div class="p-4">
                        <h4 class="font-semibold text-gray-800 mb-2 line-clamp-2">${video.title}</h4>
                        <p class="text-sm text-gray-600">${video.channelTitle}</p>
                    </div>
                `;
                videoContainer.appendChild(videoCard);
            });
        } catch (error) {
            console.error('Error fetching videos:', error);
            videoContainer.innerHTML = '<p class="text-gray-600">Could not load related videos at this time.</p>';
        }
    }
});
