# Read country names into an array
read_countries() {
    local country
    while IFS= read -r country || [[ -n "$country" ]]; do
        countries+=("$country")
    done
}


read_countries

# Concatenate the array with itself twice
concatenated_countries=("${countries[@]}" "${countries[@]}" "${countries[@]}")

# Display the concatenated array
echo "${concatenated_countries[*]}"
