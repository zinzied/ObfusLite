"""
DNA Sequence Mapping for Python Code Obfuscation
Maps code to DNA sequences using biological encoding principles
"""

import random
import base64
import json
from typing import Dict, Any, List, Tuple
from .base import BaseEncoder

class DnaEncoder(BaseEncoder):
    """
    DNA-based encoder that maps code to DNA sequences
    using biological encoding principles and genetic algorithms
    """

    def __init__(self):
        # DNA base mappings
        self.base_to_binary = {
            'A': '00',  # Adenine
            'T': '01',  # Thymine
            'G': '10',  # Guanine
            'C': '11'   # Cytosine
        }

        self.binary_to_base = {v: k for k, v in self.base_to_binary.items()}

        # Codon table for amino acid encoding (simplified)
        self.codon_table = {
            'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L',
            'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S',
            'TAT': 'Y', 'TAC': 'Y', 'TAA': '*', 'TAG': '*',
            'TGT': 'C', 'TGC': 'C', 'TGA': '*', 'TGG': 'W',
            'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',
            'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
            'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
            'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
            'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'ATG': 'M',
            'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
            'AAT': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
            'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
            'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V',
            'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
            'GAT': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
            'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G'
        }

        # Reverse codon table
        self.amino_to_codons = {}
        for codon, amino in self.codon_table.items():
            if amino not in self.amino_to_codons:
                self.amino_to_codons[amino] = []
            self.amino_to_codons[amino].append(codon)

    def encode(self, data: str) -> Dict[str, Any]:
        """
        Encode string data using DNA sequence mapping
        """
        # Convert to binary
        binary_data = ''.join(format(ord(char), '08b') for char in data)

        # Pad to multiple of 2 for DNA base encoding
        while len(binary_data) % 2 != 0:
            binary_data += '0'

        # Convert binary to DNA sequence
        dna_sequence = self._binary_to_dna(binary_data)

        # Apply genetic mutations for obfuscation
        mutated_sequence, mutation_map = self._apply_mutations(dna_sequence)

        # Create complementary strand
        complement_strand = self._create_complement(mutated_sequence)

        # Generate introns (non-coding sequences) for steganography
        introns = self._generate_introns(len(mutated_sequence))

        # Splice introns into the sequence
        spliced_sequence = self._splice_introns(mutated_sequence, introns)

        # Convert to amino acid sequence
        amino_sequence = self._dna_to_amino_acids(spliced_sequence)

        # Encode as base64 for storage
        encoded_data = base64.b64encode(json.dumps({
            'primary_sequence': spliced_sequence,
            'complement': complement_strand,
            'amino_sequence': amino_sequence
        }).encode()).decode()

        return {
            'encoded': encoded_data,
            'metadata': {
                'mutation_map': mutation_map,
                'intron_positions': introns,
                'original_length': len(data),
                'sequence_length': len(dna_sequence)
            }
        }

    def decode(self, encoded_data: Any, metadata: Dict[str, Any]) -> str:
        """
        Decode DNA sequence back to original string
        """
        # Decode from base64
        sequence_data = json.loads(base64.b64decode(encoded_data.encode()).decode())

        # Extract primary sequence
        spliced_sequence = sequence_data['primary_sequence']

        # Remove introns
        clean_sequence = self._remove_introns(spliced_sequence, metadata['intron_positions'])

        # Reverse mutations
        original_sequence = self._reverse_mutations(clean_sequence, metadata['mutation_map'])

        # Convert DNA back to binary
        binary_data = self._dna_to_binary(original_sequence)

        # Convert binary to string
        original_data = self._binary_to_string(binary_data, metadata['original_length'])

        return original_data

    def _binary_to_dna(self, binary_data: str) -> str:
        """Convert binary data to DNA sequence"""
        dna_sequence = ""
        for i in range(0, len(binary_data), 2):
            binary_pair = binary_data[i:i+2]
            dna_sequence += self.binary_to_base[binary_pair]
        return dna_sequence

    def _dna_to_binary(self, dna_sequence: str) -> str:
        """Convert DNA sequence to binary data"""
        binary_data = ""
        for base in dna_sequence:
            binary_data += self.base_to_binary[base]
        return binary_data

    def _apply_mutations(self, dna_sequence: str) -> Tuple[str, List[Dict]]:
        """Apply genetic mutations for additional obfuscation"""
        mutated = list(dna_sequence)
        mutation_map = []

        # Apply point mutations (substitutions)
        num_mutations = max(1, len(dna_sequence) // 20)  # 5% mutation rate
        mutation_positions = random.sample(range(len(dna_sequence)), num_mutations)

        for pos in mutation_positions:
            original_base = mutated[pos]
            bases = ['A', 'T', 'G', 'C']
            bases.remove(original_base)
            new_base = random.choice(bases)
            mutated[pos] = new_base

            mutation_map.append({
                'position': pos,
                'original': original_base,
                'mutated': new_base,
                'type': 'substitution'
            })

        return ''.join(mutated), mutation_map

    def _reverse_mutations(self, mutated_sequence: str, mutation_map: List[Dict]) -> str:
        """Reverse the applied mutations"""
        sequence = list(mutated_sequence)

        for mutation in mutation_map:
            if mutation['type'] == 'substitution':
                sequence[mutation['position']] = mutation['original']

        return ''.join(sequence)

    def _create_complement(self, dna_sequence: str) -> str:
        """Create complementary DNA strand"""
        complement_map = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
        return ''.join(complement_map[base] for base in dna_sequence)

    def _generate_introns(self, sequence_length: int) -> List[Dict]:
        """Generate intron sequences for steganographic hiding"""
        introns = []
        num_introns = random.randint(2, 5)

        for i in range(num_introns):
            # Generate random intron sequence
            intron_length = random.randint(10, 30)
            intron_sequence = ''.join(random.choices(['A', 'T', 'G', 'C'], k=intron_length))

            # Random insertion position
            position = random.randint(0, sequence_length)

            introns.append({
                'position': position,
                'sequence': intron_sequence,
                'length': intron_length
            })

        # Sort by position for proper insertion
        introns.sort(key=lambda x: x['position'])

        return introns

    def _splice_introns(self, sequence: str, introns: List[Dict]) -> str:
        """Splice introns into the DNA sequence"""
        spliced = sequence
        offset = 0

        for intron in introns:
            pos = intron['position'] + offset
            spliced = spliced[:pos] + intron['sequence'] + spliced[pos:]
            offset += intron['length']

        return spliced

    def _remove_introns(self, spliced_sequence: str, introns: List[Dict]) -> str:
        """Remove introns from the spliced sequence"""
        sequence = spliced_sequence

        # Remove introns in reverse order to maintain positions
        for intron in reversed(introns):
            start_pos = intron['position']
            end_pos = start_pos + intron['length']

            # Adjust for previous removals
            for prev_intron in introns:
                if prev_intron['position'] < intron['position']:
                    start_pos -= prev_intron['length']
                    end_pos -= prev_intron['length']

            sequence = sequence[:start_pos] + sequence[end_pos:]

        return sequence

    def _dna_to_amino_acids(self, dna_sequence: str) -> str:
        """Convert DNA sequence to amino acid sequence"""
        amino_acids = []

        # Process in codons (groups of 3)
        for i in range(0, len(dna_sequence) - 2, 3):
            codon = dna_sequence[i:i+3]
            if codon in self.codon_table:
                amino_acids.append(self.codon_table[codon])
            else:
                amino_acids.append('X')  # Unknown amino acid

        return ''.join(amino_acids)

    def _binary_to_string(self, binary_data: str, original_length: int) -> str:
        """Convert binary data back to string"""
        # Ensure binary data is multiple of 8
        while len(binary_data) % 8 != 0:
            binary_data += '0'

        chars = []
        for i in range(0, len(binary_data), 8):
            byte = binary_data[i:i+8]
            if len(byte) == 8:
                chars.append(chr(int(byte, 2)))

        result = ''.join(chars)
        return result[:original_length]
